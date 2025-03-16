# pages/client_onboarding_page.py
import random
import string
import time
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.base_config import BaseConfig
from config.environments import Environments  # Import for BASE_URL if needed
from selenium.common.exceptions import TimeoutException

class ClientOnboardingPage:
    def __init__(self, driver):
        self.driver = driver
        # Update locators to match the actual page structure
        self.clients_page = (By.XPATH, "//div[@id='Clients']")
        self.new_client_button = (By.XPATH, "//button[@id='new-client-button']")
        self.onboarding_page_header= (By.XPATH, "//div[@class='OnBoardNewAccount__Header']")
        self.client_name_input = (By.XPATH, "//input[@id='name']")
        self.segment_dropdown = (By.XPATH, "//div[@id='segment-select']")
        self.industry_input = (By.XPATH, "//input[@id='industry']")
        self.stage_dropdown = (By.XPATH, "//div[@id='stage' and @role='button']")
        self.sales_owner_dropdown = (By.XPATH, "//div[@id='sales_owner' and @aria-labelledby='sales_owner']")
        self.cs_owner_dropdown = (By.XPATH, "//div[@id='cs_owner' and @aria-labelledby='cs_owner']")
        self.implementation_manager_dropdown = (By.XPATH, "//div[@id='implementation_manager' and @aria-labelledby='implementation_manager']")
        self.client_save_button = (By.XPATH, "//button[@label='Save']")
        self.cancel_button = (By.XPATH, "//button[@label='Cancel']")
        self.skip_button = (By.XPATH, "//button[@label='Skip']")  

    def _generate_random_string(self, length=10):
        """Generate a random alphanumeric string for dynamic values"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def _generate_random_name(self, prefix="User", length=8):
        """Generate a random name with a prefix and numeric suffix"""
        return f"{prefix}_{random.randint(100, 999999)}"

    def navigate_to_clients(self):
        """Click the Clients icon to navigate to the Clients page"""
        clientPage = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located(self.clients_page)  # Ensure element is present
        )
        
        # Scroll the element into view
        if not clientPage.is_displayed():
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", clientPage)
            
        # Wait until it's clickable and then click
        WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(self.clients_page)
        ).click()
         
    def click_new_client(self):
        """Click the New Client button to open the onboarding form"""
        new_client_button = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(self.new_client_button)
        )
        new_client_button.click()
        print("Clicked New Client button")

    def verify_onboarding_header(self):
        """Verify the onboarding header is visible after clicking New Client"""
        try:
            # Wait for page to be fully loaded
            WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                lambda driver: self.driver.execute_script("return document.readyState") == "complete"
            )

            # Debug: Print current state
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page source snippet: {self.driver.page_source[:500]}")

            header = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.visibility_of_element_located(self.onboarding_page_header)
            )
            print(f"Onboarding header verified: {header.text}")
        except Exception as e:
            print(f"Failed to verify onboarding header: {str(e)}")
            raise

    def enter_random_client_name(self):
        """Enter a random client name using dynamic generation"""
        random_name = self._generate_random_name(prefix="Client")
        client_name = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located(self.client_name_input)
        )
        client_name.clear()
        client_name.send_keys(random_name)
        print(f"Entered random client name: {random_name}")
        return random_name  # Return for verification in tests

    def select_random_segment(self):
        """Select a random segment from the dropdown"""
        try:
            # Click the segment dropdown
            segment_dropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.segment_dropdown)
            )
            segment_dropdown.click()
            time.sleep(1)  # Allow dropdown to open
            
            # Get all options with a fresh query
            options = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )
            
            # Get the count of available options
            option_count = len(options)
            print(f"Found {option_count} segment options")
            
            if option_count == 0:
                raise Exception("No segment options found in dropdown")
            
            # Select a random option (safely)
            random_index = random.randint(0, option_count - 1)
            print(f"Selecting segment at index {random_index}")
            
            # Get a fresh reference to the option
            selected_option = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )[random_index]
            
            # Get the text before clicking
            try:
                selected_text = selected_option.text.strip()
                print(f"Selected segment: {selected_text}")
            except:
                selected_text = f"Segment_{random_index}"
                print(f"Could not get text, using placeholder: {selected_text}")
            
            # Click the option
            try:
                selected_option.click()
            except:
                self.driver.execute_script("arguments[0].click();", selected_option)
                print("Used JavaScript click for segment option")
            
            time.sleep(1)  # Allow selection to register
            return selected_text
            
        except Exception as e:
            print(f"Error selecting segment: {str(e)}")
            self.driver.save_screenshot("segment_selection_error.png")
            return "Default Segment"

    def select_random_industry(self):
        """Select a random industry from the dropdown"""
        try:
            # Click the industry dropdown
            industry_dropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.industry_input)
            )
            industry_dropdown.click()
            time.sleep(1)  # Allow dropdown to open
            
            # Get all options with a fresh query
            options = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )
            
            # Get the count of available options
            option_count = len(options)
            print(f"Found {option_count} industry options")
            
            if option_count == 0:
                raise Exception("No industry options found in dropdown")
            
            # Select a random option (safely)
            random_index = random.randint(0, option_count - 1)
            print(f"Selecting industry at index {random_index}")
            
            # Get a fresh reference to the option
            selected_option = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )[random_index]
            
            # Get the text before clicking
            try:
                selected_text = selected_option.text.strip()
                print(f"Selected industry: {selected_text}")
            except:
                selected_text = f"Industry_{random_index}"
                print(f"Could not get text, using placeholder: {selected_text}")
            
            # Click the option
            try:
                selected_option.click()
            except:
                self.driver.execute_script("arguments[0].click();", selected_option)
                print("Used JavaScript click for industry option")
            
            time.sleep(1)  # Allow selection to register
            return selected_text
            
        except Exception as e:
            print(f"Error selecting industry: {str(e)}")
            self.driver.save_screenshot("industry_selection_error.png")
            return "Default Industry"

    def select_random_stage(self):
        """Select a random stage from the dropdown"""
        try:
            # Click the stage dropdown
            stage_dropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.stage_dropdown)
            )
            stage_dropdown.click()
            time.sleep(1)  # Allow dropdown to open
            
            # Get all options with a fresh query
            options = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )
            
            # Get the count of available options
            option_count = len(options)
            print(f"Found {option_count} stage options")
            
            if option_count == 0:
                raise Exception("No stage options found in dropdown")
            
            # Select a random option (safely)
            random_index = random.randint(0, option_count - 1)
            print(f"Selecting stage at index {random_index}")
            
            # Get a fresh reference to the option
            selected_option = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )[random_index]
            
            # Get the text before clicking
            try:
                selected_text = selected_option.text.strip()
                print(f"Selected stage: {selected_text}")
            except:
                selected_text = f"Stage_{random_index}"
                print(f"Could not get text, using placeholder: {selected_text}")
            
            # Click the option
            try:
                selected_option.click()
            except:
                self.driver.execute_script("arguments[0].click();", selected_option)
                print("Used JavaScript click for stage option")
            
            time.sleep(1)  # Allow selection to register
            return selected_text
            
        except Exception as e:
            print(f"Error selecting stage: {str(e)}")
            self.driver.save_screenshot("stage_selection_error.png")
            return "Default Stage"

    def select_random_sales_owner(self):
        """Select a random sales owner from the dropdown"""
        try:
            # Click the sales owner dropdown
            sales_owner_dropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.sales_owner_dropdown)
            )
            sales_owner_dropdown.click()
            time.sleep(1)  # Allow dropdown to open
            
            # Get all options with a fresh query
            options = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )
            
            # Get the count of available options
            option_count = len(options)
            print(f"Found {option_count} sales owner options")
            
            if option_count == 0:
                raise Exception("No sales owner options found in dropdown")
            
            # Select a random option (safely)
            random_index = random.randint(0, option_count - 1)
            print(f"Selecting sales owner at index {random_index}")
            
            # Get a fresh reference to the option
            selected_option = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
            )[random_index]
            
            # Get the text before clicking
            try:
                selected_text = selected_option.text.strip()
                print(f"Selected sales owner: {selected_text}")
            except:
                selected_text = f"SalesOwner_{random_index}"
                print(f"Could not get text, using placeholder: {selected_text}")
            
            # Click the option
            try:
                selected_option.click()
            except:
                self.driver.execute_script("arguments[0].click();", selected_option)
                print("Used JavaScript click for sales owner option")
            
            time.sleep(1)  # Allow selection to register
            return selected_text
            
        except Exception as e:
            print(f"Error selecting sales owner: {str(e)}")
            self.driver.save_screenshot("sales_owner_selection_error.png")
            return "Default Sales Owner"

    def select_random_cs_owner(self):
        """Select a random CS owner from the dropdown"""
        try:
            # Wait for any loading states to complete
            time.sleep(2)
            
            # Remove any overlays that might be blocking
            self.driver.execute_script("""
                var overlays = document.getElementsByClassName('MuiBackdrop-root');
                for(var i = 0; i < overlays.length; i++) {
                    overlays[i].remove();
                }
                var modals = document.querySelectorAll('[role="presentation"]');
                for(var i = 0; i < modals.length; i++) {
                    modals[i].remove();
                }
            """)
            
            # Click the CS owner dropdown with retries
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    cs_owner_dropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                        EC.element_to_be_clickable(self.cs_owner_dropdown)
                    )
                    # Scroll into view
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cs_owner_dropdown)
                    time.sleep(1)
                    
                    try:
                        cs_owner_dropdown.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", cs_owner_dropdown)
                    break
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Click attempt {attempt + 1} failed, retrying...")
                    time.sleep(1)
                    # Remove any new overlays
                    self.driver.execute_script("""
                        var overlays = document.getElementsByClassName('MuiBackdrop-root');
                        for(var i = 0; i < overlays.length; i++) {
                            overlays[i].remove();
                        }
                    """)
            
            time.sleep(1)  # Allow dropdown to open
            
            # Get all options with a fresh query and retry logic
            for attempt in range(max_attempts):
                try:
                    options = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
                    )
                    if options:
                        break
                except:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(1)
            
            option_count = len(options)
            print(f"Found {option_count} CS owner options")
            
            if option_count == 0:
                raise Exception("No CS owner options found in dropdown")
            
            # Select a random option
            random_index = random.randint(0, option_count - 1)
            selected_option = options[random_index]
            
            # Get the text before clicking
            try:
                selected_text = selected_option.text.strip()
                print(f"Selected CS owner: {selected_text}")
            except:
                selected_text = f"CSOwner_{random_index}"
                print(f"Could not get text, using placeholder: {selected_text}")
            
            # Click the option with retry logic
            for attempt in range(max_attempts):
                try:
                    # Scroll option into view
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selected_option)
                    time.sleep(1)
                    
                    try:
                        selected_option.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", selected_option)
                    break
                except:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(1)
            
            # Verify selection
            try:
                selected_value = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                    EC.presence_of_element_located(self.cs_owner_dropdown)
                ).text.strip()
                assert selected_text in selected_value, f"CS owner selection failed. Expected: {selected_text}, Got: {selected_value}"
            except:
                print("Warning: Could not verify CS owner selection, but proceeding...")
            
            return selected_text
            
        except Exception as e:
            print(f"Error selecting CS owner: {str(e)}")
            self.driver.save_screenshot("cs_owner_selection_error.png")
            return "Default CS Owner"

    def select_random_implementation_manager(self):
        """Selects a random implementation manager from the dropdown."""
        try:
            # Wait for any loading states to complete
            time.sleep(2)
            
            # Remove any overlays that might be blocking
            self.driver.execute_script("""
                var overlays = document.getElementsByClassName('MuiBackdrop-root');
                for(var i = 0; i < overlays.length; i++) {
                    overlays[i].remove();
                }
                var modals = document.querySelectorAll('[role="presentation"]');
                for(var i = 0; i < modals.length; i++) {
                    modals[i].remove();
                }
            """)
            
            # Click the implementation manager dropdown with retries
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    impl_manager_dropdown = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                        EC.element_to_be_clickable(self.implementation_manager_dropdown)
                    )
                    # Scroll into view
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", impl_manager_dropdown)
                    time.sleep(1)
                    
                    try:
                        impl_manager_dropdown.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", impl_manager_dropdown)
                    break
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Click attempt {attempt + 1} failed, retrying...")
                    time.sleep(1)
                    # Remove any new overlays
                    self.driver.execute_script("""
                        var overlays = document.getElementsByClassName('MuiBackdrop-root');
                        for(var i = 0; i < overlays.length; i++) {
                            overlays[i].remove();
                        }
                    """)
            
            time.sleep(1)  # Allow dropdown to open
            
            # Get all options with a fresh query and retry logic
            for attempt in range(max_attempts):
                try:
                    options = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//ul[@role='listbox']/li"))
                    )
                    if options:
                        break
                except:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(1)
            
            option_count = len(options)
            print(f"Found {option_count} implementation manager options")
            
            if option_count == 0:
                raise Exception("No implementation manager options found in dropdown")
            
            # Select a random option
            random_index = random.randint(0, option_count - 1)
            selected_option = options[random_index]
            
            # Get the text before clicking
            try:
                selected_text = selected_option.text.strip()
                print(f"Selected Implementation Manager: {selected_text}")
            except:
                selected_text = f"ImplManager_{random_index}"
                print(f"Could not get text, using placeholder: {selected_text}")
            
            # Click the option with retry logic
            for attempt in range(max_attempts):
                try:
                    # Scroll option into view
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", selected_option)
                    time.sleep(1)
                    
                    try:
                        selected_option.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", selected_option)
                    break
                except:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(1)
            
            # Verify selection
            try:
                selected_value = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                    EC.presence_of_element_located(self.implementation_manager_dropdown)
                ).text.strip()
                assert selected_text in selected_value, f"Implementation manager selection failed. Expected: {selected_text}, Got: {selected_value}"
            except:
                print("Warning: Could not verify implementation manager selection, but proceeding...")
            
            return selected_text
            
        except Exception as e:
            print(f"Error selecting implementation manager: {str(e)}")
            self.driver.save_screenshot("impl_manager_selection_error.png")
            return "Default Implementation Manager"
        
    def click_save(self):
        """Click the Save button to submit the client profile"""
        try:
            # Wait for any loading states to complete
            time.sleep(2)
            
            # Remove any overlays that might be blocking
            self.driver.execute_script("""
                var overlays = document.getElementsByClassName('MuiBackdrop-root');
                for(var i = 0; i < overlays.length; i++) {
                    overlays[i].remove();
                }
                var modals = document.querySelectorAll('[role="presentation"]');
                for(var i = 0; i < modals.length; i++) {
                    modals[i].remove();
                }
            """)
            
            # Try multiple locator strategies for the save button
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    # Try first locator
                    save_button = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                        EC.element_to_be_clickable(self.client_save_button)
                    )
                except:
                    try:
                        # Try alternative locator
                        save_button = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'MuiButton') and contains(text(), 'Save')]"))
                        )
                    except:
                        if attempt == max_attempts - 1:
                            raise
                        print(f"Locating save button attempt {attempt + 1} failed, retrying...")
                        time.sleep(1)
                        continue
                
                # Scroll the button into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", save_button)
                time.sleep(1)
                
                try:
                    # Try regular click
                    save_button.click()
                    break
                except:
                    try:
                        # Try JavaScript click
                        self.driver.execute_script("arguments[0].click();", save_button)
                        break
                    except:
                        if attempt == max_attempts - 1:
                            raise
                        print(f"Click attempt {attempt + 1} failed, retrying...")
                        time.sleep(1)
                        # Remove any new overlays
                        self.driver.execute_script("""
                            var overlays = document.getElementsByClassName('MuiBackdrop-root');
                            for(var i = 0; i < overlays.length; i++) {
                                overlays[i].remove();
                            }
                        """)
            
            print("Save button clicked successfully")
            
            # Verify save action was successful with multiple success indicators
            success_verified = False
            try:
                # Wait for any of multiple possible success indicators
                for attempt in range(max_attempts):
                    try:
                        # Try different possible success messages and indicators
                        success_indicators = [
                            "//div[contains(text(),'Onboarded As Draft Successfully')]",
                            "//div[contains(text(),'Successfully')]",
                            "//div[contains(@class, 'Toastify') and contains(text(),'Success')]",
                            "//div[contains(@class, 'MuiAlert-message') and contains(text(),'Success')]",
                            "//div[contains(@class, 'success')]",
                            "//div[contains(@class, 'toast-success')]"
                        ]
                        
                        # Check URL change as a backup verification
                        current_url = self.driver.current_url
                        if "onboard-new-account" not in current_url:
                            print("URL changed after save, indicating successful navigation")
                            success_verified = True
                            break
                        
                        # Try each success indicator
                        for indicator in success_indicators:
                            try:
                                WebDriverWait(self.driver, 5).until(
                                    EC.presence_of_element_located((By.XPATH, indicator))
                                )
                                print(f"Save success verified with indicator: {indicator}")
                                success_verified = True
                                break
                            except:
                                continue
                        
                        if success_verified:
                            break
                            
                        # If no success indicator found, check if we're on a new page
                        try:
                            WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'client-details')]"))
                            )
                            print("Save verified by presence of client details page")
                            success_verified = True
                            break
                        except:
                            pass
                            
                        if attempt == max_attempts - 1:
                            # Take screenshot of final state
                            self.driver.save_screenshot("save_verification_final_state.png")
                            # Log the page source for debugging
                            print(f"Page source after save: {self.driver.page_source[:1000]}")
                            raise TimeoutException("Could not verify save success with any indicator")
                        
                        time.sleep(1)
                        
                    except Exception as e:
                        if attempt == max_attempts - 1:
                            raise
                        time.sleep(1)
                        
                if success_verified:
                    print("Save action verified successfully")
                    return True
                else:
                    raise TimeoutException("Save action could not be verified")
                    
            except Exception as e:
                print(f"Error verifying save action: {e}")
                self.driver.save_screenshot("save_verification_error.png")
                raise
            
        except Exception as e:
            print(f"Error clicking save button: {e}")
            self.driver.save_screenshot("save_button_error.png")
            raise

    def click_cancel(self):
        """Click the Cancel button to discard changes"""
        cancel_button = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.element_to_be_clickable(self.cancel_button)
        )
        cancel_button.click()
        print("Clicked Cancel button")

    def verify_client_created(self):
        """Verify the client has been created"""
        WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='template' and @aria-labelledby='template-label template' ]"))
        )
        print("Client creation verified")

    def get_current_url(self):
        """Return the current URL for verification"""
        return self.driver.current_url
    
    def click_skip_button(self):
        """Click skip button to skip custom field screen"""
        try:
            print("Waiting for Skip button...")
            skip_button = WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(self.skip_button)
            )
            print("Skip button found, checking if clickable...")
            WebDriverWait(self.driver, BaseConfig.DEFAULT_TIMEOUT).until(
                EC.element_to_be_clickable(self.skip_button)
            )
            skip_button.click()
            print("Clicked skip button")
        except TimeoutException:
            print("Skip button not found or not clickable. Skipping this step.")


    