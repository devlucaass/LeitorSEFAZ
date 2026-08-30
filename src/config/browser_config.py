from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class BrowserConfig:

    @staticmethod
    def configure_firefox(headless=False):
        options = FirefoxOptions()
        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("layout.css.devPixelsPerPx", "0.7")

        if headless:
            options.add_argument("--headless")

        return BrowserConfig._create_driver_firefox(options)

    @staticmethod
    def configure_chrome(headless=False):
        options = ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--force-device-scale-factor=0.7")

        if headless:
            options.add_argument("--headless")

        return BrowserConfig._create_driver_chrome(options)

    @staticmethod
    def configure_edge(headless=False):
        options = EdgeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--force-device-scale-factor=0.7")

        if headless:
            options.add_argument("--headless")

        return BrowserConfig._create_driver_edge(options)

    @staticmethod
    def _create_driver_firefox(options):
        return webdriver.Firefox(options=options)

    @staticmethod
    def _create_driver_chrome(options):
        return webdriver.Chrome(options=options)

    @staticmethod
    def _create_driver_edge(options):
        return webdriver.Edge(options=options)


