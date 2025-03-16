# utilities/driver_setup.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.base_config import BaseConfig

class DriverSetup:
    def __init__(self, browser=BaseConfig.BROWSER, headless=BaseConfig.HEADLESS):
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
        # Add support for other browsers if needed (e.g., Firefox)
        elif browser == "firefox":
            self.driver = webdriver.Firefox()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        self.driver.maximize_window()

    def get_driver(self):
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()