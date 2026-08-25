from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SefazClient:
    def __init__(self):
        self.driver = None

    def configure_browser(self, url, headless=False):
        options = Options()
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("layout.css.devPixelsPerPx", "0.7")

        if headless:
            options.add_argument("--headless")

        self.driver = webdriver.Firefox(options=options)
        self.driver.maximize_window()
        self.driver.get(url)

    def enter_access_key(self, access_key):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "chave"))
        ).send_keys(access_key)
        self._click_recaptcha()
        self._click_consult_button()

    def collect_data(self):
        try:
            self._wait_for_results()

            rows = self.driver.find_elements(By.CSS_SELECTOR, "#tabResult tbody tr")

            date = self._get_issue_date()
            establishment_name = self._get_establishment_name()

            data = []

            for row in rows:
                if not row.find_elements(By.CLASS_NAME, "txtTit"):
                    continue

                product_data = self._extract_product_data(row, date, establishment_name)

                data.append(product_data)

            return data

        except TimeoutException as e:
            print(f"Erro ao coletar dados: {e}")
            return []

        finally:
            self._close_browser()

    @staticmethod
    def _convert_to_number(value):
        return float(value.replace(".", "").replace(",", "."))

    def _close_browser(self):
        if self.driver:
            self.driver.quit()

    def _click_recaptcha(self):
        iframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//iframe[contains(@title,'reCAPTCHA')]")
            )
        )
        self.driver.switch_to.frame(iframe)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))
        ).click()
        WebDriverWait(self.driver, 600).until(
            lambda d: (
                d.find_element(By.ID, "recaptcha-anchor").get_attribute("aria-checked")
                == "true"
            )
        )

        self.driver.switch_to.default_content()

    def _click_consult_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Consultar')]")
            )
        ).click()

    def _wait_for_results(self):
        WebDriverWait(self.driver, 600, poll_frequency=1).until(
            EC.presence_of_element_located((By.ID, "tabResult"))
        )
        WebDriverWait(self.driver, 60, poll_frequency=1).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "txtTit"))
        )

    def _get_issue_date(self):
        date = self.driver.find_element(
            By.XPATH, '//strong[contains(text(), "Data de Emissão")]/parent::li'
        ).text
        date = (
            date.split("Data de Emissão:")[-1]
            .split("\n")[0]
            .split(" - ")[0]
            .strip()
            .split(" ")[0]
        )

        return date

    def _get_establishment_name(self):
        return self.driver.find_element(By.ID, "u20").text

    def _extract_product_data(self, row, date, establishment_name):
        product = row.find_element(By.CLASS_NAME, "txtTit").text

        quantity = row.find_element(By.CLASS_NAME, "Rqtd").text
        quantity = quantity.replace("Qtde.:", "").strip()
        quantity = self._convert_to_number(quantity)

        unit = row.find_element(By.CLASS_NAME, "RUN").text
        unit = unit.replace("UN:", "").strip()

        unit_price = row.find_element(By.CLASS_NAME, "RvlUnit").text
        unit_price = unit_price.split(":")[-1].strip()
        unit_price = self._convert_to_number(unit_price)

        total_price = row.find_element(By.XPATH, "./td[2]").text
        total_price = total_price.split("\n")[-1].strip()
        total_price = self._convert_to_number(total_price)

        return {
            "date": date,
            "establishment_name": establishment_name,
            "product": product,
            "unit": unit,
            "purchased_quantity": "-",
            "unit_price": unit_price,
            "quantity": quantity,
            "total_price": total_price,
        }
