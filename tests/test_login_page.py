import unittest
from selenium import webdriver
from pages.login_page import LoginPage
from config.base_config import BaseConfig
from config.credentials import Credentials
from config.environments import Environments

class TestLoginPage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up WebDriver before running tests"""
        cls.driver = webdriver.Chrome(BaseConfig.CHROME_DRIVER_PATH)
        cls.driver.maximize_window()

    def setUp(self):
        """Initialize the LoginPage before each test"""
        self.login_page = LoginPage(self.driver)
        self.login_page.open()

    def test_valid_login(self):
        """Test login with valid credentials"""
        self.login_page.enter_email(Credentials.VALID_EMAIL)
        self.login_page.enter_password(Credentials.VALID_PASSWORD)
        self.login_page.click_login()
        self.assertTrue(self.login_page.verify_login(), "Valid login failed!")

    def test_invalid_email(self):
        """Test login with an invalid email"""
        self.login_page.enter_email("invalid@example.com")
        self.login_page.enter_password(Credentials.VALID_PASSWORD)
        self.login_page.click_login()
        self.assertNotEqual(self.login_page.get_current_url(), Environments.HOME_PAGE_URL, "Invalid email login should fail!")

    def test_invalid_password(self):
        """Test login with an incorrect password"""
        self.login_page.enter_email(Credentials.VALID_EMAIL)
        self.login_page.enter_password("WrongPassword123")
        self.login_page.click_login()
        self.assertNotEqual(self.login_page.get_current_url(), Environments.HOME_PAGE_URL, "Invalid password login should fail!")

    def test_blank_email(self):
        """Test login with an empty email field"""
        self.login_page.enter_email("")
        self.login_page.enter_password(Credentials.VALID_PASSWORD)
        self.login_page.click_login()
        self.assertNotEqual(self.login_page.get_current_url(), Environments.HOME_PAGE_URL, "Blank email login should fail!")

    def test_blank_password(self):
        """Test login with an empty password field"""
        self.login_page.enter_email(Credentials.VALID_EMAIL)
        self.login_page.enter_password("")
        self.login_page.click_login()
        self.assertNotEqual(self.login_page.get_current_url(), Environments.HOME_PAGE_URL, "Blank password login should fail!")

    def test_blank_email_and_password(self):
        """Test login with both email and password fields empty"""
        self.login_page.enter_email("")
        self.login_page.enter_password("")
        self.login_page.click_login()
        self.assertNotEqual(self.login_page.get_current_url(), Environments.HOME_PAGE_URL, "Blank credentials login should fail!")

    def test_special_characters_email(self):
        """Test login with special characters in the email"""
        self.login_page.enter_email("!@#$%^&*()")
        self.login_page.enter_password(Credentials.VALID_PASSWORD)
        self.login_page.click_login()
        self.assertNotEqual(self.login_page.get_current_url(), Environments.HOME_PAGE_URL, "Special character email login should fail!")

    def test_sql_injection_attempt(self):
        """Test login with SQL injection-like input"""
        self.login_page.enter_email("' OR '1'='1")
        self.login_page.enter_password("' OR '1'='1")
        self.login_page.click_login()
        self.assertNotEqual(self.login_page.get_current_url(), Environments.HOME_PAGE_URL, "SQL injection attempt should fail!")

    def test_xss_attempt(self):
        """Test login with an XSS script"""
        self.login_page.enter_email("<script>alert('XSS')</script>")
        self.login_page.enter_password(Credentials.VALID_PASSWORD)
        self.login_page.click_login()
        self.assertNotEqual(self.login_page.get_current_url(), Environments.HOME_PAGE_URL, "XSS attempt should fail!")

    def tearDown(self):
        """Reset session after each test"""
        self.driver.delete_all_cookies()
        self.driver.refresh()

    @classmethod
    def tearDownClass(cls):
        """Close WebDriver after all tests"""
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
