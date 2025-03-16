# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.environments import Environments
from config.credentials import Credentials
from config.base_config import BaseConfig
from selenium.common.exceptions import TimeoutException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Define locators as tuples (By locator strategy, value)
        self.email_field = (By.ID, "user_email")
        self.password_field = (By.ID, "password")
        self.login_button = (By.XPATH, "//button[contains(text(), 'Login')]")
        self.profile_button = (By.XPATH, "//div[@class='css-axqrh9']/following-sibling::button")

    def open(self):
        """Navigate to the CogniSaaS login page"""
        self.driver.get(Environments.DEFAULT_ENV)
        print("Opened CogniSaaS login page")

    def enter_email(self, email=Credentials.VALID_EMAIL):
        """Enter email into the email field"""
        email_element = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located(self.email_field)
        )
        email_element.clear()  # Clear any pre-filled text
        email_element.send_keys(email)
        print(f"Entered email: {email}")

    def enter_password(self, password=Credentials.VALID_PASSWORD):
        """Enter password into the password field"""
        password_element = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located(self.password_field)
        )
        password_element.clear()
        password_element.send_keys(password)
        print("Entered password")

    def click_login(self):
        """Click the login button"""
        login_button = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(self.login_button)
        )
        login_button.click()
        print("Clicked login button")

    def verify_login(self):
        """Verify successful login by checking for the profile button"""
        try:
            # Wait for page load
            WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(self.profile_button)
            )
            
            # Wait for element to be clickable
            WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.profile_button)
            )
            
            # Additional check for any loading spinners to disappear
            loading_spinner = (By.CSS_SELECTOR, ".loading-spinner")  # adjust selector as needed
            WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.invisibility_of_element_located(loading_spinner)
            )
            
            return True
        except TimeoutException as e:
            print("Login verification failed - Profile button not clickable")
            raise e

    def get_current_url(self):
        """Return the current URL for verification"""
        return self.driver.current_url