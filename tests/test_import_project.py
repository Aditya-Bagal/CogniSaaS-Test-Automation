import time
import unittest
from config.credentials import Credentials
from pages.login_page import LoginPage
from pages.project_import_page import ProjectImportPageCase
from utilities.driver_setup import DriverSetup
from utilities.logger import setup_logger
from selenium.webdriver.common.by import By


class TestProjectImport(unittest.TestCase):
    def setUp(self):
        self.logger = setup_logger(log_name="Project_import_test")
        self.driver_setup = DriverSetup()
        self.driver = self.driver_setup.get_driver()
        
        self.login_page = LoginPage(self.driver)
        self.project_import_page = ProjectImportPageCase(self.driver)
        
        # Perform login
        self.logger.info("Logging in for project import test")
        self.login_page.open()
        self.login_page.enter_email(Credentials.VALID_EMAIL)
        self.login_page.enter_password(Credentials.VALID_PASSWORD)
        self.login_page.click_login()
        self.login_page.verify_login()
        self.logger.info("Login successful")
    
    def tearDown(self):
        self.driver.quit()
        self.logger.info("Teardown complete: WebDriver closed")
    
    def test_import_project(self):
        """Testing import a project from project page"""
        self.logger.info("Starting project import")
        
        # Navigate to project page
        self.project_import_page.navigate_to_projects_page()
        self.logger.info("Navigated to project page")
        
        time.sleep(2)
        self.project_import_page.click_new_project()
        self.logger.info("Clicked new project button")

        # Wait for "Onboarded As Draft Successfully!" toast to disappear
        # self.project_import_page.wait_for_element_invisibility(self.client_onboarding_toast)

        project_template = self.project_import_page.select_project_template()
        self.logger.info(f"Project Template: {project_template}")

        delivery_manager = self.project_import_page.select_project_delivery_manager()
        self.logger.info(f"Delivery Manager: {delivery_manager}")
         
        project_priority = self.project_import_page.select_project_priority()
        self.logger.info(f"Project Priority: {project_priority}")
        
        project_category = self.project_import_page.select_category()
        self.logger.info(f"Project Category: {project_category}")
        
        project_stage = self.project_import_page.select_stage()
        self.logger.info(f"Project Stage: {project_stage}")

        # Fill out project import details
        project_client_name = self.project_import_page.select_client()
        self.logger.info(f"Selected client: {project_client_name}")
        
        project_name = self.project_import_page.enter_random_project_name()
        self.logger.info(f"Project Name: {project_name}")
        
        # project_planned_start_date = self.project_import_page.select_random_planned_start_date()
        # self.logger.info(f"Planned Start Date: {project_planned_start_date}")
        
        # project_planned_end_date = self.project_import_page.select_random_planned_end_date()
        # self.logger.info(f"Planned End Date: {project_planned_end_date}")
        
        project_teammate = self.project_import_page.select_teammate()
        self.logger.info(f"Project Teammate: {project_teammate}")
        
        project_implementation_fee = self.project_import_page.enter_random_implementation_fee()
        self.logger.info(f"Implementation Fee: {project_implementation_fee}")
        
        project_arr = self.project_import_page.enter_random_arr()
        self.logger.info(f"ARR: {project_arr}")
        
        project_description = self.project_import_page.enter_random_project_description()
        self.logger.info(f"Project Description: {project_description}")
        
        # Save project
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]").click()
        self.logger.info("Clicked Save button")


        time.sleep(5)


if __name__ == "__main__":
    unittest.main()
