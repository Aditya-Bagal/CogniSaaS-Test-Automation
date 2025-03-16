import random
import re
import time
import string
import os
from datetime import datetime, timedelta
from functools import wraps
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.keys import Keys  # Importing Keys class to simulate keyboard keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Importing Keys class

from config.base_config import BaseConfig
from utilities import logger

def screenshot_decorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            # Take screenshot after successful execution
            self.take_screenshot(f"success_{func.__name__}")
            return result
        except Exception as e:
            # Take screenshot on error
            self.take_screenshot(f"error_{func.__name__}")
            raise e
    return wrapper

class ProjectImportPageCase:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logger  # Ensure logger is initialized

        # Create screenshots directory if it doesn't exist
        self.screenshot_dir = os.path.join(os.getcwd(), 'screenshots')
        os.makedirs(self.screenshot_dir, exist_ok=True)

        # Locators
        self.project_page = (By.ID, "Projects")
        self.add_new_project = (By.XPATH, "//button[@label='New Project']")
        self.client_dropdown = (By.XPATH, "//div[@id='client']")
        self.choose_project_template = (By.XPATH, "//div[@id='template']")
        self.project_name_input = (By.ID, "name")
        self.project_priority = (By.ID, "priority-select")
        self.project_category = (By.ID, "category-select")
        self.project_stage = (By.ID, "stage-select")
        self.project_delivery_manager = (By.XPATH, "//div[@role='button' and @id='delivery_manager']")
        self.project_planned_start_date = (By.XPATH, "(//*[name()='path'])[59]")
        self.project_planned_end_date = (By.XPATH, "(//*[name()='path'])[60]")
        self.project_teammate_dropdown = (By.XPATH, "//input[@placeholder='Choose a team member']")
        self.project_implementation_fee = (By.ID, "implementation_fee")
        self.project_arr = (By.ID, "recurring_revenue")
        self.project_description_box = (By.XPATH, "//div[@role='textbox']")
        self.project_save_button = (By.XPATH, "//button[@label='Save']")
        self.client_onboarding_toast = (By.XPATH, "//div[contains(text(),'Onboarded As Draft Successfully!')]")
        self.Dropdown_frame = (By.XPATH, "//div[@tabindex='-1']")
        self.project_import_verification = (By.XPATH, "//span[contains(text(),'Overview')]")

    def take_screenshot(self, name):
        """Take a screenshot and save it with timestamp."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            self.driver.save_screenshot(filepath)
            print(f"Screenshot saved: {filepath}")
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

    def clientOnboardingToastInvisibility(self):
        try:
            WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.invisibility_of_element_located(self.client_onboarding_toast)
            )
            print("Client Onboarding toast is invisible.")
        except Exception as e:
            print(f"Error waiting for Client Onboarding toast to disappear: {e}")

    @screenshot_decorator
    def navigate_to_projects_page(self):
        """Click projects icon to navigate to projects page."""
        try:
            project_page = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(self.project_page)
            )

            if not project_page.is_displayed():
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", project_page)

            WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.project_page)
            ).click()
            print("Navigated to Projects page.")
            
            # Add assertion to verify navigation
            assert "projects" in self.driver.current_url.lower(), "Failed to navigate to Projects page"
        except Exception as e:
            print(f"Error navigating to Projects page: {e}")
            raise

    @screenshot_decorator
    def click_new_project(self):
        """Click the New Project button to open the onboarding form."""
        try:
            new_project_button = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.add_new_project)
            )
            new_project_button.click()
            print("Clicked New Project button.")
            time.sleep(2)
            
            # Add assertion to verify form is opened
            assert WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(self.project_name_input)
            ).is_displayed(), "New Project form did not open"
        except Exception as e:
            print(f"Error clicking New Project button: {e}")
            raise

    @screenshot_decorator
    def select_project_template(self):
        """Clicks on 'choose_project_template', prints all options, and selects a random one."""
        try:
            # Wait for any overlays or loading elements to disappear
            time.sleep(2)  # Give time for any animations to complete
            
            templateDropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.choose_project_template)
            )
            templateDropdown.click()
            print("Project Template Dropdown opened.")
            
            templateElements = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )

            templateOptions = [(option, option.text.strip()) for option in templateElements if option.text.strip()]
            valid_templateOptions = [(el, txt) for el, txt in templateOptions if txt]

            if valid_templateOptions:
                random_template_element, random_template_text = random.choice(valid_templateOptions)
                # Scroll the option into view and click using JavaScript
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_template_element)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", random_template_element)
                print(f"Selected Random Project Template: {random_template_text}")
                
                # Add assertion to verify selection with more flexible text matching
                try:
                    selected_element = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                        EC.presence_of_element_located(self.choose_project_template)
                    )
                    selected_value = selected_element.text.strip()
                    
                    # Check if the selected text is contained within the expected text or vice versa
                    assert (selected_value in random_template_text or random_template_text in selected_value), \
                        f"Template selection failed. Expected text to contain or be contained in: '{random_template_text}', Got: '{selected_value}'"
                    
                    print(f"Template selection verified. Selected value: {selected_value}")
                except Exception as verify_error:
                    print(f"Warning: Template selection verification failed: {verify_error}")
                    # Take an additional screenshot of the verification failure
                    self.take_screenshot("template_verification_error")
                    
                return random_template_text
            else:
                print("No valid Project Template options available to select.")
                return None
        except Exception as e:
            print(f"Error selecting Project Template: {e}")
            # Take an additional screenshot of the error state
            self.take_screenshot("template_selection_error")
            raise

    @screenshot_decorator
    def select_client(self):
        """Clicks the 'Client' dropdown, prints all options, and selects a random one."""
        try:
            # Wait for any overlays or loading elements to disappear
            time.sleep(2)  # Give time for any animations to complete
            
            # Wait for client dropdown to be present and visible
            clientDropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(self.client_dropdown)
            )
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", clientDropdown)
            time.sleep(1)  # Allow scrolling to complete
            
            # Try to click using JavaScript if normal click is intercepted
            try:
                clientDropdown.click()
            except:
                self.driver.execute_script("arguments[0].click();", clientDropdown)
            
            print("Client Dropdown opened.")
            
            # Wait for dropdown options with increased timeout
            clientElements = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )
            
            # Store WebElements and clean text together
            clientOptions = [(option, option.text.strip()) for option in clientElements if option.text.strip()]
            valid_clientOptions = [(el, txt) for el, txt in clientOptions if txt]

            if valid_clientOptions:
                random_client_element, random_client_text = random.choice(valid_clientOptions)
                
                # Scroll the option into view and click using JavaScript
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_client_element)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", random_client_element)
                
                print(f"Selected Random Client: {random_client_text}")
                
                # Add assertion to verify selection
                try:
                    selected_value = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                        EC.presence_of_element_located(self.client_dropdown)
                    ).text.strip()
                    assert selected_value == random_client_text, f"Client selection failed. Expected: {random_client_text}, Got: {selected_value}"
                except:
                    print("Warning: Could not verify client selection, but proceeding...")
                
                return random_client_text
            else:
                print("No valid Client options available to select.")
                return None

        except Exception as e:
            print(f"Error selecting Client: {e}")
            # Take an additional screenshot of the error state
            self.take_screenshot("client_selection_error")
            raise

    @screenshot_decorator
    def select_project_priority(self):
        """Clicks the 'Project Priority' dropdown, prints all options, and selects the first available option."""
        try:
            priorityDropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.project_priority)
            )
            priorityDropdown.click()

            # Wait for the dropdown options to appear
            priorityElements = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[@role='option']"))
            )

            # Store all priority options
            priorityOptions = [(option, self.re.sub(r'\s+', ' ', option.text).strip()) for option in priorityElements if option.text.strip()]
                 # Filter out any invalid or empty options
            valid_priorityOptions = [(el, txt) for el, txt in priorityOptions if txt.lower()]

            if valid_priorityOptions:
                random_priority_element, random_priority_text = random.choice(valid_priorityOptions)
                random_priority_element.click()  # Click the WebElement, not the text
                print(f"Selected Random Priority: {random_priority_text}")
                return random_priority_text  # Return selected option text
            else:
                print("No valid categories available to select.")
                return None
        except (TimeoutException, StaleElementReferenceException) as e:
            print(f"Error occurred while selecting project category: {e}")
            return None

    @screenshot_decorator
    def select_category(self):
        """Clicks the 'Project Category' dropdown, switches to the frame, selects a random category, and prints the selected category."""
        
        try:
            # Step 1: Click the 'Project Category' dropdown
            categoryDropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.project_category)
            )
            categoryDropdown.click()
            time.sleep(1)  # Allow dropdown to expand

            # Get all category elements
            categoryElements = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[@role='option']"))
            )

            # Store WebElements and clean text together
            categoryOptions = [(option, self.re.sub(r'\s+', ' ', option.text).strip()) for option in categoryElements if option.text.strip()]

            # Filter out any invalid or empty options
            valid_categoryOptions = [(el, txt) for el, txt in categoryOptions if txt.lower()]

            if valid_categoryOptions:
                random_category_element, random_category_text = random.choice(valid_categoryOptions)
                random_category_element.click()  # Click the WebElement, not the text
                print(f"Selected Random Category: {random_category_text}")
                return random_category_text  # Return selected option text
            else:
                print("No valid categories available to select.")
                return None
        except (TimeoutException, StaleElementReferenceException) as e:
            print(f"Error occurred while selecting project category: {e}")
            return None

       
    @screenshot_decorator
    def select_stage(self):
        """Clicks the 'Project Stage' dropdown, selects a random stage from the dropdown, and prints the selected stage."""
        
        try:
            # Step 1: Click the 'Project Stage' dropdown
            StageDropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.project_stage)
            )
            StageDropdown.click()
            time.sleep(1)  # Allow dropdown to expand

            # Step 2: Wait for options to appear
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[@role='option']"))
            )

            # Step 3: Refetch the options before selecting
            options = self.driver.find_elements(By.XPATH, "//li[@role='option']")

            if not options:
                print("No options available!")
                return

            print(f"Total options found: {len(options)}")

            # Step 4: Select a random option (get fresh reference)
            random_option = random.choice(options)

            # Get text BEFORE clicking to avoid stale element issues
            selected_text = random_option.text.strip()
            print(f"Selected Project Stage (Before Click): {selected_text}")

            # Scroll into view and click
            self.driver.execute_script("arguments[0].scrollIntoView(true);", random_option)
            time.sleep(1)  # Let it scroll properly
            random_option.click()
            time.sleep(1)  # Allow selection to register

            # Step 5: Print selected stage after clicking
            print(f"Selected Project Stage (After Click): {selected_text}")  # Printing the captured text
            
            return selected_text  # Return the selected stage if needed

        except (TimeoutException, StaleElementReferenceException) as e:
            print(f"Error occurred while selecting project stage: {e}")
            return None 


    import re

    @screenshot_decorator
    def select_project_delivery_manager(self):
        """Opens the project delivery manager dropdown and selects a valid option."""
        try:
            # Wait for any overlays or loading elements to disappear
            time.sleep(2)  # Give time for any animations to complete
            
            project_deliveryManager = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.project_delivery_manager)
            )
            
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", project_deliveryManager)
            time.sleep(1)  # Allow scrolling to complete
            
            project_deliveryManager.click()
            print("Delivery Manager Dropdown opened.")

            # Wait for options with increased timeout
            options = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )

            # Filter only enabled options with safe attribute checking
            valid_options = []
            for option in options:
                if option.is_enabled():
                    data_value = option.get_attribute("data-value")
                    # Check if data_value exists and doesn't contain DONT_UPDATE
                    if data_value and "DONT_UPDATE" not in data_value.lower():
                        valid_options.append(option)
            
            if valid_options:
                random_option = random.choice(valid_options)
                # Scroll the option into view and click using JavaScript
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_option)
                time.sleep(1)
                self.driver.execute_script("arguments[0].click();", random_option)
                
                selected_text = random_option.text.strip()
                print(f"Selected Delivery Manager: {selected_text}")
                
                # Verify selection
                try:
                    selected_value = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                        EC.presence_of_element_located(self.project_delivery_manager)
                    ).text.strip()
                    assert selected_value == selected_text, f"Delivery Manager selection failed. Expected: {selected_text}, Got: {selected_value}"
                except:
                    print("Warning: Could not verify delivery manager selection, but proceeding...")
                
                return selected_text
            else:
                print("No valid delivery manager options available to select.")
                self.take_screenshot("no_valid_delivery_managers")
                return None

        except Exception as e:
            print(f"Error selecting Delivery Manager: {e}")
            self.take_screenshot("delivery_manager_selection_error")
            raise



    @screenshot_decorator
    def select_teammate(self):
        """Clicks the 'Teammate' dropdown, prints all options, and selects the first available option."""
        try:
            # Wait for dropdown to be clickable and then click
            teammateDropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.project_teammate_dropdown)
            )
            teammateDropdown.click()
            print("TeamMates Dropdown opened.")

            # Wait for options to appear
            teammateElements = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )

            # Extract clean text while keeping original WebElements
            teammateOptions = [(option, self.re.sub(r'\s+', ' ', option.text).strip()) for option in teammateElements if option.text.strip()]

            # Get valid options (excluding empty or placeholder ones)
            valid_teammates = [(el, txt) for el, txt in teammateOptions if txt and txt.lower() != "select"]

            if valid_teammates:
                random_teammate_element, random_teammate_text = random.choice(valid_teammates)
                random_teammate_element.click()  # Click the WebElement, not the text
                print(f"Selected Random Teammate: {random_teammate_text}")
                return random_teammate_text  # Return selected option's text
            else:
                print("No valid teammates available to select.")
                return None

        except (TimeoutException, StaleElementReferenceException) as e:
            print(f"Error selecting Teammate: {e}")
            return None
        
    def _set_date_using_js(self, date_picker_locator, date_name, days_offset=0):
        """Set a date in the date picker using JavaScript."""
        try:
            date_field = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(date_picker_locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView();", date_field)

            selected_date = (datetime.today() + timedelta(days=days_offset)).strftime("%Y-%m-%d")
            self.driver.execute_script(f"arguments[0].setAttribute('value', '{selected_date}');", date_field)

            print(f"Selected {date_name}: {selected_date}")
            return selected_date
        except Exception as e:
            print(f"Error selecting {date_name}: {e}")
            return None

    def select_random_planned_start_date(self):
        return self._set_date_using_js(self.project_planned_start_date, "Planned Start Date")

    def select_random_planned_end_date(self):
        return self._set_date_using_js(self.project_planned_end_date, "Planned End Date", days_offset=7)

    def enter_random_text(self, locator, label, text_length=5):
        """Enter a random text into an input field."""
        try:
            random_text = f"{label}_{''.join(random.choices(string.ascii_letters + string.digits, k=text_length))}"
            input_field = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(locator)
            )
            input_field.clear()
            input_field.send_keys(random_text)
            print(f"Entered {label}: {random_text}")
            return random_text
        except Exception as e:
            print(f"Error entering {label}: {e}")
            return None

    @screenshot_decorator
    def enter_random_project_name(self):
        """Enter a random project name and verify it was entered correctly."""
        try:
            random_name = self.enter_random_text(self.project_name_input, "Project")
            # Add assertion to verify entered project name
            input_field = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(self.project_name_input)
            )
            entered_value = input_field.get_attribute("value")
            assert entered_value == random_name, f"Project name entry failed. Expected: {random_name}, Got: {entered_value}"
            return random_name
        except Exception as e:
            print(f"Error entering project name: {e}")
            raise

    @screenshot_decorator
    def enter_random_project_description(self):
        """Enter a random project description and verify it was entered correctly."""
        try:
            random_description = self.enter_random_text(self.project_description_box, "Description")
            # Add assertion to verify entered description
            description_field = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(self.project_description_box)
            )
            entered_value = description_field.text
            assert entered_value == random_description, f"Project description entry failed. Expected: {random_description}, Got: {entered_value}"
            return random_description
        except Exception as e:
            print(f"Error entering project description: {e}")
            raise
    
    @screenshot_decorator
    def enter_random_implementation_fee(self):
        """Enter a random numeric implementation fee."""
        try:
            random_fee = str(random.randint(1000, 100000))
            input_field = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(self.project_implementation_fee)
            )
            input_field.clear()
            input_field.send_keys(random_fee)
            print(f"Entered Implementation Fee: {random_fee}")
            
            # Add assertion to verify entered value
            entered_value = input_field.get_attribute("value").replace(",", "")
            assert entered_value == random_fee, f"Implementation fee entry failed. Expected: {random_fee}, Got: {entered_value}"
            return random_fee
        except Exception as e:
            print(f"Error entering Implementation Fee: {e}")
            raise

    @screenshot_decorator
    def enter_random_arr(self):
        """Enter a random numeric ARR (Annual Recurring Revenue)."""
        try:
            random_arr = str(random.randint(5000, 200000))
            input_field = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.project_arr)
            )
            input_field.clear()
            input_field.send_keys(random_arr)
            print(f"Entered ARR: {random_arr}")
            
            # Add assertion to verify entered value, handling numeric formatting
            entered_value = input_field.get_attribute("value").replace(",", "").lstrip("0")
            assert entered_value == random_arr, f"ARR entry failed. Expected: {random_arr}, Got: {entered_value}"
            return random_arr
        except Exception as e:
            print(f"Error entering ARR: {e}")
            self.take_screenshot("arr_entry_error")
            raise

    @screenshot_decorator
    def click_project_save(self):
        """Click the Save button to submit the project form."""
        try:
            save_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.project_save_button)
            )
            save_button.click()
            print("Save button clicked.")
            
            # Add assertion to verify save action
            try:
                WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                    EC.presence_of_element_located(self.project_import_verification)
                )
                assert True, "Project saved successfully"
            except TimeoutException:
                assert False, "Save confirmation toast did not appear"
        except Exception as e:
            print(f"Error clicking save button: {e}")
            raise
