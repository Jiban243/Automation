# import pandas as pd
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
# import time
# import os
# import sys
# import logging

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("gnps_automation.log"),
#         logging.StreamHandler(sys.stdout)
#     ]
# )
# logger = logging.getLogger("GNPSAutomation")

# def setup_driver():
#     """Set up and return a configured Chrome webdriver."""
#     chrome_options = Options()
#     # Uncomment the line below if you want to run in headless mode
#     # chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--window-size=1920,1080")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--disable-extensions")
#     # Add user agent to appear more like a regular browser
#     chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36")
    
#     # Create the Chrome driver
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.maximize_window()
    
#     # Set page load timeout
#     driver.set_page_load_timeout(30)
    
#     return driver

# def login_to_gnps(driver, username, password):
#     """Login to GNPS website."""
#     try:
#         # Navigate directly to the login page
#         driver.get("https://gnps.ucsd.edu/ProteoSAFe/user/login.jsp")
#         print("✅ Navigated directly to GNPS login page")
        
#         # Wait for username and password fields to be present
#         wait = WebDriverWait(driver, 15)  # Increased timeout for slower connections
#         username_field = wait.until(EC.presence_of_element_located((By.NAME, "user")))
#         password_field = driver.find_element(By.NAME, "password")
        
#         # Print found elements for debugging
#         print(f"Username field found: {username_field}")
        
#         # Enter credentials with explicit waits between actions
#         username_field.clear()
#         time.sleep(1)
#         username_field.send_keys(username)
#         time.sleep(1)
#         password_field.clear()
#         time.sleep(1)
#         password_field.send_keys(password)
#         print("✅ Entered login credentials")
#         time.sleep(1)
        
#         # Click the login button - try different potential selectors
#         try:
#             login_button = driver.find_element(By.NAME, "login")
#             login_button.click()
#         except NoSuchElementException:
#             try:
#                 login_button = driver.find_element(By.XPATH, "//input[@type='submit' and @value='login']")
#                 login_button.click()
#             except NoSuchElementException:
#                 # Try clicking by form submission
#                 password_field.submit()
                
#         print("✅ Clicked login button")
        
#         # Wait longer for login to complete
#         time.sleep(10)
        
#         # Save screenshot for debugging
#         driver.save_screenshot("after_login.png")
#         print(f"Current URL after login: {driver.current_url}")
        
#         # Check if login was successful - more comprehensive checks
#         if any(indicator in driver.current_url for indicator in ["user=", "ProteoSAFe/index", "logged"]):
#             print("✅ Login successful")
#             return True
#         else:
#             # Try to check if we're in a logged-in state by looking for elements
#             try:
#                 # Look for any element that would indicate successful login
#                 wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Welcome') or contains(@class, 'user-info')]")))
#                 print("✅ Login successful (detected via page elements)")
#                 return True
#             except:
#                 print("❌ Login failed - could not detect login success indicators")
#                 return False
            
#     except Exception as e:
#         print(f"❌ Login process failed: {e}")
#         driver.save_screenshot("login_error.png")
#         return False

# def navigate_to_molecular_networking(driver):
#     """Navigate to the molecular networking form."""
#     try:
#         # Navigate to the workflow selection page
#         driver.get("https://gnps.ucsd.edu/ProteoSAFe/index.jsp")
#         wait = WebDriverWait(driver, 15)
        
#         # Save screenshot to see the page state
#         driver.save_screenshot("workflow_page.png")
#         print(f"Current URL: {driver.current_url}")
        
#         # Try multiple approaches to find and click the molecular networking link
#         try:
#             # # First try direct link text
#             # networking_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Click Here here to run a demo molecular")))
#             # networking_link.click()
#             # Locate the button by its value and the associated span's ID
#             button = driver.find_element(By.XPATH, "//div[@id='spec_on_server']//input[@type='button' and @value='Select Input Files']")

#             # Click the button
#             button.click()
#             print("✅ Clicked molecular networking link using LINK_TEXT")
#         except (TimeoutException, NoSuchElementException):
#             try:
#                 # Try partial link text
#                 networking_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "demo molecular")))
#                 networking_link.click()
#                 print("✅ Clicked molecular networking link using PARTIAL_LINK_TEXT")
#             except (TimeoutException, NoSuchElementException):
#                 try:
#                     # Try XPath with contains
#                     networking_link = wait.until(EC.element_to_be_clickable((
#                         By.XPATH, "//a[contains(text(), 'molecular') or contains(@href, 'molecular')]")))
#                     networking_link.click()
#                     print("✅ Clicked molecular networking link using XPath")
#                 except (TimeoutException, NoSuchElementException):
#                     # Try to navigate directly to the known URL
#                     print("⚠️ Could not find molecular networking link, trying direct URL navigation")
#                     driver.get("https://gnps.ucsd.edu/ProteoSAFe/index.jsp?params={%22workflow%22:%22MOLECULAR-NETWORKING%22}")
                    
#         # Wait for the page to load
#         time.sleep(5)
#         driver.save_screenshot("after_navigation.png")
        
#         # Verify we're on the right page
#         if any(indicator in driver.current_url for indicator in ["MOLECULAR-NETWORKING", "molecular", "networking"]):
#             print("✅ Successfully navigated to molecular networking page")
#             return True
#         else:
#             # Try to detect if we're on the right page by looking for specific elements
#             try:
#                 wait.until(EC.presence_of_element_located((
#                     By.XPATH, "//*[contains(text(), 'Spectrum Files') or contains(text(), 'Mass Tolerance')]")))
#                 print("✅ Successfully navigated to molecular networking page (detected via elements)")
#                 return True
#             except:
#                 print("❌ Failed to navigate to molecular networking page")
#                 return False
                
#     except Exception as e:
#         print(f"❌ Navigation to molecular networking failed: {e}")
#         driver.save_screenshot("navigation_error.png")
#         return False

# def upload_spectrum_files(driver, file_paths):
#     """Upload spectrum files to the form."""
#     try:
#         wait = WebDriverWait(driver, 10)
        
#         # Find the spectrum files upload button
#         upload_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Select Input Files']")))
#         upload_button.click()
#         print("✅ Clicked on spectrum files upload button")
        
#         # Wait for file upload dialog
#         time.sleep(3)
        
#         # Here you'd typically interact with the file upload dialog
#         # Since it's a system dialog, Selenium can't directly interact with it
#         # You'd need to use tools like pyautogui or set the file path directly
        
#         # For demonstration, let's assume we're setting the file path directly
#         # (This would need to be adapted based on actual page structure)
#         file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        
#         # Upload multiple files if provided
#         if isinstance(file_paths, list):
#             for file_path in file_paths:
#                 file_input.send_keys(file_path)
#                 time.sleep(1)
#         else:
#             file_input.send_keys(file_paths)
            
#         print("✅ Selected spectrum files")
        
#         # Click upload or confirm button
#         confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Upload') or contains(text(), 'Confirm')]")))
#         confirm_button.click()
#         print("✅ Confirmed file upload")
        
#         return True
        
#     except Exception as e:
#         print(f"❌ File upload failed: {e}")
#         return False

# def set_spectrum_parameters(driver, precursor_tolerance=2.0, fragment_tolerance=0.5):
#     """Set spectrum parameters in the form."""
#     try:
#         wait = WebDriverWait(driver, 15)
        
#         # Save screenshot to see the form state
#         driver.save_screenshot("parameters_form.png")
        
#         # Try different approaches to find and set the precursor tolerance field
#         precursor_selectors = [
#             (By.XPATH, "//input[@value='2.0']"),
#             (By.XPATH, "//input[contains(@name, 'precursor')]"),
#             (By.XPATH, "//td[contains(text(), 'Precursor')]/following-sibling::td//input"),
#             (By.XPATH, "//label[contains(text(), 'Precursor')]/following-sibling::input")
#         ]
        
#         for selector_type, selector_value in precursor_selectors:
#             try:
#                 precursor_field = wait.until(EC.presence_of_element_located((selector_type, selector_value)))
#                 # Use JavaScript to set the value for more reliability
#                 driver.execute_script("arguments[0].value = '';", precursor_field)
#                 precursor_field.send_keys(str(precursor_tolerance))
#                 print(f"✅ Set precursor ion mass tolerance to {precursor_tolerance}")
#                 break
#             except (TimeoutException, NoSuchElementException):
#                 continue
#         else:
#             print("⚠️ Could not set precursor ion mass tolerance")
        
#         # Try different approaches to find and set the fragment tolerance field
#         fragment_selectors = [
#             (By.XPATH, "//input[@value='0.5']"),
#             (By.XPATH, "//input[contains(@name, 'fragment')]"),
#             (By.XPATH, "//td[contains(text(), 'Fragment')]/following-sibling::td//input"),
#             (By.XPATH, "//label[contains(text(), 'Fragment')]/following-sibling::input")
#         ]
        
#         for selector_type, selector_value in fragment_selectors:
#             try:
#                 fragment_field = wait.until(EC.presence_of_element_located((selector_type, selector_value)))
#                 # Use JavaScript to set the value for more reliability
#                 driver.execute_script("arguments[0].value = '';", fragment_field)
#                 fragment_field.send_keys(str(fragment_tolerance))
#                 print(f"✅ Set fragment ion mass tolerance to {fragment_tolerance}")
#                 break
#             except (TimeoutException, NoSuchElementException):
#                 continue
#         else:
#             print("⚠️ Could not set fragment ion mass tolerance")
        
#         # Take a screenshot after setting parameters
#         driver.save_screenshot("after_setting_parameters.png")
        
#         return True
        
#     except Exception as e:
#         print(f"❌ Setting parameters failed: {e}")
#         driver.save_screenshot("parameters_error.png")
#         return False

# def process_massive_ids(excel_file):
#     """Process MassIVE IDs from Excel file."""
#     try:
#         # Load Excel file
#         df = pd.read_excel(excel_file)
#         unique_massive_ids = df["attribute_MassIVE"].dropna().unique()
#         print(f"✅ Loaded {len(unique_massive_ids)} unique MassIVE IDs from Excel")
        
#         # Initialize driver
#         driver = setup_driver()
        
#         # Login to GNPS - retry logic for login
#         max_login_attempts = 3
#         login_attempt = 0
#         login_successful = False
        
#         while login_attempt < max_login_attempts and not login_successful:
#             login_attempt += 1
#             print(f"Login attempt {login_attempt} of {max_login_attempts}")
#             login_successful = login_to_gnps(driver, username="jiban", password="Lpwr62BD@")
#             if not login_successful and login_attempt < max_login_attempts:
#                 print("Retrying login...")
#                 driver.delete_all_cookies()
#                 time.sleep(3)
        
#         if not login_successful:
#             print("❌ All login attempts failed. Exiting.")
#             driver.quit()
#             return
        
#         # Print current cookies for debugging
#         print("Cookies after login:")
#         for cookie in driver.get_cookies():
#             print(f"  {cookie['name']}: {cookie['value'][:10]}...")
        
#         # Process each MassIVE ID
#         for massive_id in unique_massive_ids:
#             try:
#                 print(f"\n📊 Processing MassIVE ID: {massive_id}")
                
#                 # Navigate to molecular networking page
#                 if not navigate_to_molecular_networking(driver):
#                     continue
                
#                 # Use the MassIVE ID to share/import files
#                 # Wait for form to load
#                 time.sleep(5)  # Increased wait time
#                 wait = WebDriverWait(driver, 15)  # Increased timeout
                
#                 # Save screenshot to verify page state
#                 driver.save_screenshot(f"molecular_networking_{massive_id}.png")
                
#                 # Try to find and click on "Share Files" tab with more robust approach
#                 try:
#                     # Try multiple potential selectors for the sharing tab
#                     selectors_to_try = [
#                         (By.ID, "sharing_tab"),
#                         (By.XPATH, "//a[contains(text(), 'Share Files')]"),
#                         (By.XPATH, "//div[contains(@class, 'tab')][contains(., 'Share')]"),
#                         (By.XPATH, "//li[contains(., 'Share Files')]")
#                     ]
                    
#                     for selector_type, selector_value in selectors_to_try:
#                         try:
#                             share_tab = wait.until(EC.element_to_be_clickable((selector_type, selector_value)))
#                             share_tab.click()
#                             print(f"✅ Clicked on Share Files tab using selector: {selector_type}='{selector_value}'")
#                             time.sleep(3)
#                             break
#                         except (TimeoutException, NoSuchElementException):
#                             continue
#                     else:
#                         print("⚠️ Could not find Share Files tab with any of the attempted selectors")
#                         driver.save_screenshot(f"share_tab_not_found_{massive_id}.png")
#                         continue
                    
#                     # Wait for form to load and interact within form context
#                     # Try multiple potential form selectors
#                     form_selectors = [
#                         (By.NAME, "sharing_importForm"),
#                         (By.XPATH, "//form[contains(@action, 'sharing')]"),
#                         (By.XPATH, "//form[contains(., 'Import')]")
#                     ]
                    
#                     for selector_type, selector_value in form_selectors:
#                         try:
#                             sharing_form = wait.until(EC.presence_of_element_located((selector_type, selector_value)))
#                             print(f"✅ Found sharing form using selector: {selector_type}='{selector_value}'")
                            
#                             # Try to find the input field with multiple selectors
#                             input_selectors = [
#                                 (By.NAME, "user"), 
#                                 (By.XPATH, "//input[@type='text']"),
#                                 (By.CSS_SELECTOR, "input[type='text']")
#                             ]
                            
#                             for input_selector_type, input_selector_value in input_selectors:
#                                 try:
#                                     input_box = sharing_form.find_element(input_selector_type, input_selector_value)
#                                     input_box.clear()
#                                     input_box.send_keys(massive_id)
#                                     print(f"✅ Entered MassIVE ID using selector: {input_selector_type}='{input_selector_value}'")
#                                     break
#                                 except NoSuchElementException:
#                                     continue
#                             else:
#                                 print("⚠️ Could not find input field for MassIVE ID")
#                                 continue
                            
#                             # Try to find the import button with multiple selectors
#                             button_selectors = [
#                                 (By.ID, "sharing_importButton"),
#                                 (By.XPATH, "//button[contains(text(), 'Import')]"),
#                                 (By.XPATH, "//input[@type='submit'][contains(@value, 'Import')]"),
#                                 (By.CSS_SELECTOR, "button.import-button")
#                             ]
                            
#                             for button_selector_type, button_selector_value in button_selectors:
#                                 try:
#                                     import_button = sharing_form.find_element(button_selector_type, button_selector_value)
#                                     import_button.click()
#                                     print(f"✅ Clicked Import button using selector: {button_selector_type}='{button_selector_value}'")
#                                     break
#                                 except NoSuchElementException:
#                                     continue
#                             else:
#                                 print("⚠️ Could not find Import button")
#                                 continue
                                
#                             print(f"✅ Successfully imported MassIVE ID: {massive_id}")
#                             time.sleep(5)  # Increased wait time after import
#                             driver.save_screenshot(f"after_import_{massive_id}.png")
#                             break
                            
#                         except (TimeoutException, NoSuchElementException):
#                             continue
#                     else:
#                         print("⚠️ Could not find sharing form with any of the attempted selectors")
                
#                 except Exception as e:
#                     print(f"⚠️ Share files process failed: {e}")
#                     driver.save_screenshot(f"share_files_error_{massive_id}.png")
#                     continue
                
#                 # Set parameters for molecular networking
#                 set_spectrum_parameters(driver)
                
#                 # Additional steps here as needed
                
#                 time.sleep(3)
                
#             except Exception as e:
#                 print(f"❌ Failed to process {massive_id}: {e}")
#                 driver.save_screenshot(f"process_error_{massive_id}.png")
                
#         # Cleanup
#         driver.quit()
#         print("✅ Processing complete")
        
#     except Exception as e:
#         print(f"❌ Excel processing failed: {e}")
#         if 'driver' in locals():
#             driver.quit()

# if __name__ == "__main__":
#     try:
#         logger.info("Starting GNPS automation script")
#         excel_file="microbe_masst_table_metadata.xlsx"
        
#         if not os.path.exists(excel_file):
#             logger.error(f"Excel file '{excel_file}' not found!")
#             sys.exit(1)
            
#         # Set custom download directory
#         download_dir = os.path.join(os.getcwd(), "gnps_downloads")
#         os.makedirs(download_dir, exist_ok=True)
#         logger.info(f"Download directory set to: {download_dir}")
        
#         # Process MassIVE IDs
#         process_massive_ids(excel_file)
        
#     except Exception as e:
#         logger.exception(f"Unhandled exception in main: {e}")
#         sys.exit(1)

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import traceback
import time

# ----------------------------
# CONFIGURATION
# ----------------------------

EXCEL_PATH = "microbe_masst_table_metadata.xlsx"  
USERNAME = "jkpatra"      
PASSWORD = "jkqr459svn"     
COLUMN_NAME = "attribute_MassIVE"

# ----------------------------
# READ MASSIVE IDS FROM EXCEL
# ----------------------------

df = pd.read_excel(EXCEL_PATH)
massive_ids = df[COLUMN_NAME].dropna().unique().tolist()

def automate_data_loader(massive_ids, USERNAME, PASSWORD):
    # ----------------------------
    # SETUP SELENIUM
    # ----------------------------

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

    try:
        # Step 1: Login to GNPS
        driver.get("https://gnps.ucsd.edu/ProteoSAFe/user/login.jsp")

        wait.until(EC.presence_of_element_located((By.NAME, "user")))
        username_input = driver.find_element(By.NAME, "user")
        password_input = driver.find_element(By.NAME, "password")

        username_input.clear()
        password_input.clear()
        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        login_button = driver.find_element(By.NAME, "login")
        login_button.click()

        # Step 2: Wait for redirection and presence of target section
        wait.until(EC.presence_of_element_located((By.ID, "spec_on_server")))

        # Step 3: Click "Select Input Files" button
        select_input_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Select Input Files']"))
        )
        select_input_button.click()

        # Step 4: Loop through each MassIVE ID
        for massive_id in massive_ids:
            try:
                print(f"🟡 Processing {massive_id}...")
                url = f"https://gnps.ucsd.edu/ProteoSAFe/upload.jsp?user={massive_id}"
                driver.get(url)
                # ✅ Click on "Share Files" tab
                wait.until(EC.element_to_be_clickable((By.ID, "sharing_tab"))).click()
                time.sleep(2)

                wait.until(EC.presence_of_element_located((By.NAME, "sharing_importForm")))
                form = driver.find_element(By.NAME, "sharing_importForm")

                input_box = form.find_element(By.NAME, "user")
                input_box.clear()
                input_box.send_keys(massive_id)

                import_button = form.find_element(By.ID, "sharing_importButton")
                import_button.click()

                print(f"✅ Success with {massive_id}")
                time.sleep(2)

            except Exception as e:
                print(f"❌ Error with {massive_id}: {type(e).__name__} - {e}")
                traceback.print_exc()
                driver.save_screenshot(f"error_{massive_id}.png")

    finally:
        print("✅ All done.")
        driver.quit()


# automate_data_loader(massive_ids, username=USERNAME, password=PASSWORD)