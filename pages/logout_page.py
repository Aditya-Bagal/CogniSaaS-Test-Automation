# pages/logout_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.base_config import BaseConfig

class LogoutPage:
    def __init__(self, driver):
        self.driver = driver
        # Define locators as tuples (By locator strategy, value)
        self.profile_button = (By.XPATH, "//div[@class='css-axqrh9']/following-sibling::button")
        self.logout_button = (By.XPATH, "//h6[contains(text(), 'Logout')]")
        self.email_field = (By.ID, "user_email")

    def click_profile(self):
        """Click the profile button to open the dropdown"""
        profile_button = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(self.profile_button)
        )
        profile_button.click()
        print("Clicked profile button")

    def click_logout(self):
        """Click the logout button"""
        logout_button = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(self.logout_button)
        )
        logout_button.click()
        print("Clicked logout button")

    def verify_logout(self):
        """Verify logout by checking for the email field on the login page"""
        WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located(self.email_field)
        )
        print("Logout verified - Back to login page")

    def get_current_url(self):
        """Return the current URL for verification"""
        return self.driver.current_url

    def is_profile_visible(self):
        """Check if the profile button is visible (useful for session verification)"""
        try:
            WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(self.profile_button)
            )
            return True
        except Exception:
            return False