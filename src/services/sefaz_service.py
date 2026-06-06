from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tkinter import messagebox


class SefazBot:

    def __init__(self, chave):
        self.driver = None
        self.chave = chave

    def configura_navegador(self, site, headless=False):

        try:
            options = Options()
            options.set_preference('dom.webnotifications.enabled', False)
            options.set_preference('layout.css.devPixelsPerPx', '0.7')

            if headless:
                options.add_argument('--headless')

            self.driver = webdriver.Firefox(options=options)
            self.driver.maximize_window()
            self.driver.get(site)

        except Exception as erro:
            messagebox.showerror('Erro', f'Ocorreu um erro ao iniciar navegador:\n{erro}')

    def digita_chave(self):

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'chave'))).send_keys(self.chave)

            iframe = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,"//iframe[contains(@title,'reCAPTCHA')]")))

            self.driver.switch_to.frame(iframe)

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor"))).click()

            WebDriverWait(self.driver, 600).until(lambda d:d.find_element(By.ID,"recaptcha-anchor").get_attribute("aria-checked") == "true")

            self.driver.switch_to.default_content()

            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//button[contains(text(), 'Consultar')]"))).click()

        except Exception as erro:
            messagebox.showerror('Erro', f'Ocorreu um erro:\n{erro}')

            self.driver.quit()

    def coleta_dados(self):

        try:
            WebDriverWait(self.driver, 600, poll_frequency=1).until(EC.presence_of_element_located((By.ID, 'tabResult')))

            WebDriverWait(self.driver, 60, poll_frequency=1 ).until(EC.presence_of_all_elements_located( (By.CLASS_NAME, 'txtTit')))

            linhas = self.driver.find_elements(By.CSS_SELECTOR,'#tabResult tbody tr')

            dados = []

            data = self.driver.find_element(By.XPATH,'//strong[contains(text(), "Data de Emissão")]/parent::li').text

            data = (data.split("Data de Emissão:")[-1].split("\n")[0].split(" - ")[0].strip().split(" ")[0])

            estabelecimento = self.driver.find_element(By.ID,'u20').text

            for linha in linhas:
                spans = linha.find_elements(By.CLASS_NAME,'txtTit')

                if spans:
                    produto = linha.find_element(By.CLASS_NAME,'txtTit').text

                    quantidade = linha.find_element(By.CLASS_NAME,'Rqtd').text

                    quantidade = (quantidade.replace('Qtde.:', '').strip())

                    quantidade = float(quantidade.replace('.', '').replace(',', '.'))

                    grandeza = linha.find_element(
                        By.CLASS_NAME,
                        'RUN'
                    ).text

                    grandeza = (
                        grandeza
                        .replace('UN:', '')
                        .strip()
                    )

                    valor_unitario = linha.find_element(
                        By.CLASS_NAME,
                        'RvlUnit'
                    ).text

                    valor_unitario = (
                        valor_unitario
                        .split(':')[-1]
                        .strip()
                    )

                    valor_unitario = float(
                        valor_unitario
                        .replace('.', '')
                        .replace(',', '.')
                    )

                    valor_total = linha.find_element(
                        By.XPATH,
                        './td[2]'
                    ).text

                    valor_total = (
                        valor_total
                        .split('\n')[-1]
                        .strip()
                    )

                    valor_total = float(
                        valor_total
                        .replace('.', '')
                        .replace(',', '.')
                    )

                    dados.append({
                        'data': data,
                        'estabelecimento': estabelecimento,
                        'produto': produto,
                        'grandeza': grandeza,
                        'quantidade_comprada': '-',
                        'valor_unitario': valor_unitario,
                        'quantidade': quantidade,
                        'valor_total': valor_total
                    })

            return dados

        except Exception as erro:

            messagebox.showerror(
                'Erro',
                f'Ocorreu um erro:\n{erro}'
            )

        finally:
            self.driver.quit()

if __name__ == "__main__":
    sefaz = SefazBot('26260205677591002950651130001034101359159580')
    sefaz.configura_navegador('https://nfce.sefaz.pe.gov.br:444/nfce/consulta', headless=False)
    sefaz.digita_chave()
    print(sefaz.coleta_dados())

    