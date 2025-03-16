import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.driver_setup import DriverSetup
from utilities.logger import setup_logger
from utilities.screenshot import capture_screenshot
from pages.login_page import LoginPage
from pages.project_import_page import ProjectImportPageCase
from pages.client_onboarding_page import ClientOnboardingPage
from config.credentials import Credentials
from config.environments import Environments

class TestClientOnboarding(unittest.TestCase):
    def setUp(self):
        self.logger = setup_logger(log_name="client_onboarding_test")
        self.driver_setup = DriverSetup()
        self.driver = self.driver_setup.get_driver()

        self.login_page = LoginPage(self.driver)
        self.client_onboarding_page = ClientOnboardingPage(self.driver)
        self.project_import_page = ProjectImportPageCase(self.driver)

        # Perform login
        self.logger.info("Logging in for client onboarding test")
        self.login_page.open()
        self.login_page.enter_email(Credentials.VALID_EMAIL)
        self.login_page.enter_password(Credentials.VALID_PASSWORD)
        self.login_page.click_login()
        self.login_page.verify_login()
        self.logger.info("Login successful")

    def tearDown(self):
        self.driver.quit()
        self.logger.info("Teardown complete: WebDriver closed")

    def test_successful_login_and_client_onboarding(self):
        """Test client onboarding process"""
        self.logger.info("Starting test: Client Onboarding")

        # Navigate to Clients page
        self.client_onboarding_page.navigate_to_clients()
        self.logger.info("Navigated to Clients page")

        # Click New Client button
        self.client_onboarding_page.click_new_client()
        self.client_onboarding_page.verify_onboarding_header()
        self.logger.info("Clicked 'New Client' button")

        # Wait for elements to be clickable
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(self.client_onboarding_page.sales_owner_dropdown)
        )

        # Fill out client onboarding details

        segment = self.client_onboarding_page.select_random_segment()
        self.logger.info(f"Segment: {segment}")

        client_name = self.client_onboarding_page.enter_random_client_name()
        self.logger.info(f"Client Name: {client_name}")

        industry = self.client_onboarding_page.select_random_industry()
        self.logger.info(f"Industry: {industry}")

        stage = self.client_onboarding_page.select_random_stage()
        self.logger.info(f"Stage: {stage}")

        sales_owner = self.client_onboarding_page.select_random_sales_owner()
        self.logger.info(f"Sales Owner: {sales_owner}")

        cs_owner = self.client_onboarding_page.select_random_cs_owner()
        self.logger.info(f"CS Owner: {cs_owner}")

        implementation_manager = self.client_onboarding_page.select_random_implementation_manager()
        self.logger.info(f"Implementation Manager: {implementation_manager}")

        # Save client
        self.client_onboarding_page.click_save()
        self.logger.info("Clicked Save button")

        # Verify client creation
        self.client_onboarding_page.verify_client_created()
        self.logger.info("Client successfully created")

        # Skip custom field screen
        self.client_onboarding_page.click_skip_button()
        self.logger.info("Clicked Skip button")

        clientOnboardingToast = self.project_import_page.clientOnboardingToastInvisibility()
        self.logger.info(f"Toast message disappeared")

        # time.sleep(2)

        # Fill out project import details
        project_template = self.project_import_page.select_project_template()
        self.logger.info(f"Project Template: {project_template}")

        project_name = self.project_import_page.enter_random_project_name()
        self.logger.info(f"Project Name: {project_name}")

        # project_priority = self.project_import_page.select_project_priority()
        # self.logger.info(f"Project Priority: {project_priority}")

        # project_category = self.project_import_page.select_category()
        # self.logger.info(f"Project Category: {project_category}")

        # project_stage = self.project_import_page.select_stage()
        # self.logger.info(f"Project Stage: {project_stage}")

        # delivery_manager = self.project_import_page.select_delivery_manager()
        # self.logger.info(f"Delivery Manager: {delivery_manager}")

        project_implementation_fee = self.project_import_page.enter_random_implementation_fee()
        self.logger.info(f"Implementation Fee: {project_implementation_fee}")

        project_arr = self.project_import_page.enter_random_arr()
        self.logger.info(f"ARR: {project_arr}")

        # project_planned_start_date = self.project_import_page.select_random_planned_start_date()
        # self.logger.info(f"Planned Start Date: {project_planned_start_date}")

        # project_planned_end_date = self.project_import_page.select_random_planned_end_date()
        # self.logger.info(f"Planned End Date: {project_planned_end_date}")

        project_teammate = self.project_import_page.select_teammate()
        self.logger.info(f"Project Teammate: {project_teammate}")

        project_description = self.project_import_page.enter_random_project_description()
        self.logger.info(f"Project Description: {project_description}")

        # Save project
        self.project_import_page.click_project_save()
        self.logger.info(f"Client {client_name} imported with'{project_name}' successfully")

if __name__ == "__main__":
    unittest.main()
