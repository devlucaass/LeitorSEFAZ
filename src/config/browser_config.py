from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class BrowserConfig:

    @staticmethod
    def configure_browser(browser_name, headless=False):
        browsers = {
            "firefox": BrowserConfig._configure_firefox,
            "chrome": BrowserConfig._configure_chrome,
            "edge": BrowserConfig._configure_edge,
        }

        return browsers[browser_name](headless)

    @staticmethod
    def _configure_firefox(headless):
        options = FirefoxOptions()

        options.set_preference("dom.webnotifications.enabled", False)

        if headless:
            options.add_argument("--headless")

        return webdriver.Firefox(options=options)

    @staticmethod
    def _configure_chrome(headless):
        options = ChromeOptions()

        options.add_argument("--disable-notifications")

        if headless:
            options.add_argument("--headless")

        return webdriver.Chrome(options=options)

    @staticmethod
    def _configure_edge(headless):
        options = EdgeOptions()

        options.add_argument("--disable-notifications")

        if headless:
            options.add_argument("--headless")

        return webdriver.Edge(options=options)



