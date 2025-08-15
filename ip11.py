import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedAlertPresentException
import traceback
import time

# ----------------------------
# CONFIGURATION
# ----------------------------

USERNAME = "jiban"         
PASSWORD = "Lpwr62BD@"     

def automate_data_deletion(USERNAME, PASSWORD):
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
        time.sleep(3)

        url = "https://gnps.ucsd.edu/ProteoSAFe/upload.jsp"
        driver.get(url)
        # Step 4: Click on "Share Files" tab
        wait.until(EC.element_to_be_clickable((By.ID, "sharing_tab"))).click()
        time.sleep(7)

        # Step 5: Navigate to the "sharing_importedUsers" div
        sharing_div = wait.until(
            EC.presence_of_element_located((By.ID, "sharing_importedUsers"))
        )

        # Step 6: Loop to find and delete divs with text starting with "[Dataset MSV0"
        while True:
            try:
                # Find all divs within sharing_importedUsers
                divs = sharing_div.find_elements(By.TAG_NAME, "div")
                found_match = False

                for div in divs:
                    try:
                        # Get the text of the div
                        div_text = div.text.strip()
                        # Check if the text starts with "[Dataset MSV0"
                        if div_text.startswith("[Dataset MSV0"):
                            found_match = True
                            # Find the image with src="images/hide.png" within this div
                            hide_img = div.find_element(
                                By.XPATH, './/img[@class="selectable" and @src="images/hide.png"]'
                            )
                            # Click the image to delete the entry
                            try:
                                hide_img.click()
                                print(f"Deleted entry: {div_text}")
                                with open("deletion_log.txt", "a") as log_file:
                                    log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Deleted entry: {div_text}\n")
                                # Wait for the element to become stale, indicating page update
                                wait.until(EC.staleness_of(hide_img))
                            except UnexpectedAlertPresentException as alert_ex:
                                # Handle the alert (e.g., 403 Forbidden)
                                alert = driver.switch_to.alert
                                alert_text = alert.text
                                print(f"Alert encountered: {alert_text}")
                                with open("deletion_log.txt", "a") as log_file:
                                    log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Alert encountered: {alert_text}\n")
                                alert.accept()  # Accept the alert to continue
                                time.sleep(1)  # Brief pause after accepting alert
                            break  # Break the for loop to refresh the div list
                    except NoSuchElementException:
                        continue  # Skip if the image is not found in this div

                if not found_match:
                    print("No more divs with text starting '[Dataset MSV0' found.")
                    break  # Exit the while loop if no matching divs are found

                # Refresh the sharing_div after deletion
                sharing_div = wait.until(
                    EC.presence_of_element_located((By.ID, "sharing_importedUsers"))
                )

            except UnexpectedAlertPresentException as alert_ex:
                # Handle unexpected alerts outside the div loop
                alert = driver.switch_to.alert
                alert_text = alert.text
                print(f"Unexpected alert encountered: {alert_text}")
                with open("deletion_log.txt", "a") as log_file:
                    log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Unexpected alert: {alert_text}\n")
                alert.accept()
                time.sleep(1)
                # Refresh the sharing_div after handling the alert
                sharing_div = wait.until(
                    EC.presence_of_element_located((By.ID, "sharing_importedUsers"))
                )
            except Exception as e:
                print(f"Error processing divs: {str(e)}")
                with open("deletion_log.txt", "a") as log_file:
                    log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error processing divs: {str(e)}\n")
                break

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        with open("deletion_log.txt", "a") as log_file:
            log_file.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] General error: {str(e)}\n")
        traceback.print_exc()

    finally:
        print(" All done.")
        driver.quit()