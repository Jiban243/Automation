# #!#!/Users/jibankrishnapatra/Downloads/IP/venv/bin/python
# import time
# import traceback
# import os
# import re
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, ElementClickInterceptedException

# USERNAME = "jibanp"
# PASSWORD = "1234567890"

# # Read folder names from cleaned_unique_paths.txt
# def load_folder_names():
#     """Load folder names from cleaned_unique_paths.txt into a set"""
#     folder_names = set()
#     try:
#         with open("cleaned_unique_paths.txt", "r", encoding="utf-8") as f:
#             for line in f:
#                 folder_name = line.strip()
#                 if folder_name:
#                     folder_names.add(folder_name)
#         print(f"✅ Loaded {len(folder_names)} folder names from cleaned_unique_paths.txt")
#         return folder_names
#     except Exception as e:
#         print(f"❌ Error loading cleaned_unique_paths.txt: {e}")
#         return set()

# FOLDER_NAMES = load_folder_names()

# # Read mzXML filenames from mzxml_file_paths.txt
# def load_mzxml_filenames():
#     """Load mzXML filenames from mzxml_file_paths.txt into a set"""
#     mzxml_filenames = set()
#     try:
#         with open("mzxml_file_paths.txt", "r", encoding="utf-8") as f:
#             for line in f:
#                 filename = line.strip()
#                 if filename and filename.endswith('.mzXML'):
#                     mzxml_filenames.add(filename)
#         print(f"✅ Loaded {len(mzxml_filenames)} mzXML filenames from mzxml_file_paths.txt")
#         return mzxml_filenames
#     except Exception as e:
#         print(f"❌ Error loading mzxml_file_paths.txt: {e}")
#         return set()

# MZXML_FILENAMES = load_mzxml_filenames()

# # Configure Chrome options for better stability
# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--window-size=1920,1080")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# driver = webdriver.Chrome(options=chrome_options)
# wait = WebDriverWait(driver, 90)

# def save_progress(node_index):
#     """Save the last successfully expanded node index to a file"""
#     with open("expansion_progress.txt", "w") as f:
#         f.write(str(node_index))

# def load_progress():
#     """Load the last successfully expanded node index from a file"""
#     if os.path.exists("expansion_progress.txt"):
#         with open("expansion_progress.txt", "r") as f:
#             return int(f.read().strip())
#     return 0

# def expand_all_nodes(max_retries=3):
#     """Expand dataset nodes first, then selectively expand folders listed in cleaned_unique_paths.txt"""
#     last_successful_node = load_progress()
    
#     # Phase 1: Expand all dataset nodes ([Dataset MSV00...])
#     iteration = 0
#     print("🔄 Phase 1: Expanding all dataset nodes...")
#     while True:
#         try:
#             dataset_icons = driver.find_elements(By.XPATH, 
#                 "//span[contains(@class, 'dijitTreeLabel') and contains(text(), '[Dataset MSV00')]/ancestor::div[contains(@class, 'dijitTreeRow')]//img[contains(@class, 'dijitTreeExpandoClosed')]")
#             if not dataset_icons:
#                 print(f"✅ No more dataset nodes to expand after iteration {iteration + 1}.")
#                 break

#             print(f"🔄 Iteration {iteration + 1}: Expanding {len(dataset_icons)} dataset nodes...")
#             for i, icon in enumerate(dataset_icons):
#                 node_index = last_successful_node + i + 1
#                 retries = max_retries
#                 while retries > 0:
#                     try:
#                         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
#                         time.sleep(0.7)
#                         label = icon.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')]//span[contains(@class, 'dijitTreeLabel')]").text.strip()
#                         icon.click()
#                         print(f"  ➕ Expanded dataset node {node_index}/{len(dataset_icons) + last_successful_node}: {label}")
#                         save_progress(node_index)
#                         time.sleep(0.7)
#                         break
#                     except (WebDriverException, StaleElementReferenceException) as e:
#                         retries -= 1
#                         print(f"  ⚠️ Could not expand dataset node {node_index} (Retry {max_retries - retries}/{max_retries}): {e}")
#                         if retries == 0:
#                             print(f"  ❌ Failed to expand dataset node {node_index} after {max_retries} retries.")
#                             continue
#                         time.sleep(3)
#             iteration += 1
#             last_successful_node += len(dataset_icons)
#             save_progress(last_successful_node)
#             time.sleep(3)
#         except WebDriverException as e:
#             print(f"❌ Error during dataset node expansion: {e}")
#             print("🔄 Attempting to recover by restarting Phase 1...")
#             time.sleep(5)
#             continue

#     # Phase 2: Expand only folders listed in cleaned_unique_paths.txt
#     iteration = 0
#     print("🔄 Phase 2: Expanding folders listed in cleaned_unique_paths.txt...")
#     while True:
#         try:
#             expand_icons = driver.find_elements(By.XPATH, "//img[contains(@class, 'dijitTreeExpandoClosed')]")
#             if not expand_icons:
#                 print(f"✅ No more folders to expand after iteration {iteration + 1}.")
#                 break

#             print(f"🔄 Iteration {iteration + 1}: Checking {len(expand_icons)} unexpanded folders...")
#             nodes_expanded = 0
#             for i, icon in enumerate(expand_icons):
#                 node_index = last_successful_node + i + 1
#                 retries = max_retries
#                 while retries > 0:
#                     try:
#                         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
#                         time.sleep(0.7)
#                         label = icon.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')]//span[contains(@class, 'dijitTreeLabel')]").text.strip()
#                         if label in FOLDER_NAMES:
#                             icon.click()
#                             print(f"  ➕ Expanded folder {node_index}/{len(expand_icons) + last_successful_node}: {label}")
#                             save_progress(node_index)
#                             nodes_expanded += 1
#                             time.sleep(0.7)
#                             break
#                         else:
#                             print(f"  ℹ️ Skipped folder {node_index}/{len(expand_icons) + last_successful_node}: {label} (not in cleaned_unique_paths.txt)")
#                             break
#                     except (WebDriverException, StaleElementReferenceException) as e:
#                         retries -= 1
#                         print(f"  ⚠️ Could not process folder {node_index} (Retry {max_retries - retries}/{max_retries}): {e}")
#                         if retries == 0:
#                             print(f"  ❌ Failed to process folder {node_index} after {max_retries} retries.")
#                             continue
#                         time.sleep(3)
#             if nodes_expanded == 0:
#                 print(f"✅ No matching folders expanded in iteration {iteration + 1}. Stopping Phase 2.")
#                 break
#             iteration += 1
#             last_successful_node += len(expand_icons)
#             save_progress(last_successful_node)
#             time.sleep(3)
#         except WebDriverException as e:
#             print(f"❌ Error during folder expansion: {e}")
#             print("🔄 Attempting to recover by restarting Phase 2...")
#             time.sleep(5)
#             continue

# def get_full_path(element):
#     """Construct the full path by traversing up to the dataset root"""
#     path_parts = []
#     current = element
#     label = "unknown"
#     try:
#         # Get the current element's label (file or folder name)
#         label = current.find_element(By.XPATH, ".//span[contains(@class, 'dijitTreeLabel')]").text.strip()
#         if label:
#             path_parts.append(label)
        
#         # Traverse up to parent dijitTreeRow elements
#         max_depth = 50
#         depth = 0
#         dataset_id = None
#         while depth < max_depth:
#             try:
#                 parent = current.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')][1]")
#                 parent_label = parent.find_element(By.XPATH, ".//span[contains(@class, 'dijitTreeLabel')]").text.strip()
#                 if parent_label:
#                     # Check for dataset root pattern [Dataset MSV00...]
#                     match = re.match(r'^\[Dataset (MSV00.*?)\]', parent_label)
#                     if match:
#                         dataset_id = match.group(1)  # Extract MSV000078547
#                         break
#                     path_parts.append(parent_label)
                
#                 # Check for child elements indicating non-root node
#                 try:
#                     parent.find_element(By.XPATH, ".//img[contains(@class, 'dijitTreeExpandoOpened')]")
#                     parent.find_element(By.XPATH, ".//span[contains(@class, 'dijitTreeContentExpanded')]")
#                 except WebDriverException:
#                     if dataset_id:
#                         break  # Reached root if dataset_id was set
#                     break  # No child elements, assume root if no dataset_id
                
#                 current = parent
#                 depth += 1
#             except (WebDriverException, StaleElementReferenceException):
#                 break
        
#         # Construct path starting with dataset_id
#         if dataset_id:
#             path_parts.reverse()
#             full_path = f"{dataset_id}/{'/'.join(path_parts)}"
#         else:
#             full_path = "/".join(reversed(path_parts)) if path_parts else "Unknown path"
        
#         return full_path
#     except (WebDriverException, StaleElementReferenceException) as e:
#         print(f"  ⚠️ Error constructing path for element '{label}': {e}")
#         try:
#             parent_tree = driver.execute_script("return arguments[0].outerHTML;", current)
#             print(f"  ℹ️ DOM context: {parent_tree[:200]}...")
#         except:
#             print("  ℹ️ Could not retrieve DOM context.")
#         return f"Error for file {label}: {str(e)}"

# def select_mzxml_files():
#     """Select .mzXML files listed in mzxml_file_paths.txt and save their full paths"""
#     try:
#         print("🔍 Searching for .mzXML files to select...")
#         mzxml_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'dijitTreeLabel') and contains(text(), '.mzXML')]")
        
#         if not mzxml_elements:
#             print("⚠️ No .mzXML files found.")
#             return False

#         if not MZXML_FILENAMES:
#             print("⚠️ No filenames loaded from mzxml_file_paths.txt. Cannot proceed.")
#             return False

#         print(f"✅ Found {len(mzxml_elements)} .mzXML files. Selecting those listed in mzxml_file_paths.txt...")
#         file_paths = []
#         selected_count = 0
#         for i, element in enumerate(mzxml_elements):
#             try:
#                 file_name = element.text.strip()
#                 if file_name not in MZXML_FILENAMES:
#                     print(f"  ℹ️ Skipped .mzXML file {i + 1}/{len(mzxml_elements)}: {file_name} (not in mzxml_file_paths.txt)")
#                     continue

#                 tree_row = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')][1]")
#                 full_path = get_full_path(tree_row)
#                 print(f"  📁 Path for .mzXML file {i + 1}/{len(mzxml_elements)}: {full_path}")
#                 file_paths.append(full_path)
                
#                 driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#                 time.sleep(0.7)
#                 element.click()
#                 print(f"  ✅ Selected .mzXML file {i + 1}/{len(mzxml_elements)}: {file_name}")
#                 selected_count += 1
#                 time.sleep(0.7)
#             except (WebDriverException, StaleElementReferenceException) as e:
#                 file_name = element.text if element.text else "unknown file"
#                 print(f"  ⚠️ Could not process .mzXML file {i + 1} ({file_name}): {e}")
#                 file_paths.append(f"Error for file {file_name}: {str(e)}")
        
#         if selected_count == 0:
#             print("⚠️ No .mzXML files from mzxml_file_paths.txt were found in the dataset tree.")
#             return False

#         try:
#             with open("mzxml_file_paths.txt", "w", encoding="utf-8") as f:
#                 for path in file_paths:
#                     f.write(f"{path}\n")
#             print("✅ Saved file paths to 'mzxml_file_paths.txt'.")
#         except Exception as e:
#             print(f"❌ Error saving paths to file: {e}")

#         return True

#     except WebDriverException as e:
#         print(f"❌ Error while selecting .mzXML files: {e}")
#         traceback.print_exc()
#         return False

# def select_tsv_files(max_retries=3, max_attempts=3):
#     """Find and expand folder containing USERNAME, recursively search for .tsv files, and click 'Metadata File' button"""
#     attempt = 1
#     while attempt <= max_attempts:
#         try:
#             print(f"🔍 Attempt {attempt}/{max_attempts}: Searching for folder containing '{USERNAME}' to expand...")
#             # List all folder names for debugging
#             folder_elements_all = driver.find_elements(By.XPATH, "//span[contains(@class, 'dijitTreeLabel')]")
#             folder_names = []
#             for elem in folder_elements_all:
#                 try:
#                     name = elem.text.strip()
#                     if name and not name.endswith(('.mzXML', '.tsv')):  # Exclude files
#                         folder_names.append(name)
#                 except:
#                     continue
#             print(f"  ℹ️ Available folders: {', '.join(folder_names[:20])}{'...' if len(folder_names) > 20 else ''}")

#             # Find unexpanded folders with USERNAME (case-insensitive)
#             expand_icons = driver.find_elements(By.XPATH, 
#                 f"//span[contains(@class, 'dijitTreeLabel') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{USERNAME.lower()}')]/ancestor::div[contains(@class, 'dijitTreeRow')]//img[contains(@class, 'dijitTreeExpandoClosed')]")
            
#             folder_found = False
#             if expand_icons:
#                 print(f"✅ Found {len(expand_icons)} unexpanded folder(s) containing '{USERNAME}'.")
#                 for i, icon in enumerate(expand_icons):
#                     retries = max_retries
#                     while retries > 0:
#                         try:
#                             driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
#                             time.sleep(0.7)
#                             label = icon.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')]//span[contains(@class, 'dijitTreeLabel')]").text.strip()
#                             icon.click()
#                             print(f"  ➕ Expanded folder {i + 1}/{len(expand_icons)}: {label}")
#                             folder_found = True
#                             time.sleep(5)  # Wait for folder content to load
#                             break
#                         except (WebDriverException, StaleElementReferenceException) as e:
#                             retries -= 1
#                             print(f"  ⚠️ Could not expand folder '{label}' (Retry {max_retries - retries}/{max_retries}): {e}")
#                             if retries == 0:
#                                 print(f"  ❌ Failed to expand folder '{label}' after {max_retries} retries.")
#                                 continue
#                             time.sleep(3)
#                     if folder_found:
#                         break
#             else:
#                 # Check if folder is already expanded
#                 folder_elements = driver.find_elements(By.XPATH, 
#                     f"//span[contains(@class, 'dijitTreeLabel') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{USERNAME.lower()}')]")
#                 if folder_elements:
#                     print(f"  ℹ️ Folder containing '{USERNAME}' is already expanded.")
#                     folder_found = True
#                 else:
#                     print(f"⚠️ No folder containing '{USERNAME}' found on attempt {attempt}.")
#                     if attempt == max_attempts:
#                         print(f"  ℹ️ Proceeding without selecting .tsv files after {max_attempts} attempts.")
#                         return True  # Allow script to continue
#                     attempt += 1
#                     time.sleep(5)
#                     continue

#             if not folder_found:
#                 print(f"❌ Could not find or expand any folder containing '{USERNAME}' on attempt {attempt}.")
#                 if attempt == max_attempts:
#                     print(f"  ℹ️ Proceeding without selecting .tsv files after {max_attempts} attempts.")
#                     return True  # Allow script to continue
#                 attempt += 1
#                 time.sleep(5)
#                 continue

#             # Recursively search for .tsv files within the expanded folder
#             print("🔍 Recursively searching for .tsv files within the expanded folder...")
#             tsv_elements = []
#             def find_tsv_elements(element):
#                 try:
#                     # Check if current element is a span with dijitTreeLabel containing .tsv
#                     if element.tag_name == "span" and "dijitTreeLabel" in element.get_attribute("class"):
#                         text = element.text.strip()
#                         if text and ".tsv" in text.lower():
#                             tsv_elements.append(element)
#                             print(f"  📍 Found .tsv file: {text}")
#                     # Recursively search all children
#                     children = element.find_elements(By.XPATH, "./*")
#                     for child in children:
#                         find_tsv_elements(child)
#                 except WebDriverException as e:
#                     print(f"  ⚠️ Error traversing DOM: {e}")

#             # Start recursion from the expanded folder's container
#             expanded_folder = driver.find_element(By.XPATH, f"//span[contains(@class, 'dijitTreeLabel') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{USERNAME.lower()}')]/ancestor::div[contains(@class, 'dijitTreeRow')]")
#             container = expanded_folder.find_element(By.XPATH, "./following-sibling::div[contains(@class, 'dijitTreeContainer')]")
#             find_tsv_elements(container)

#             if not tsv_elements:
#                 print("⚠️ No .tsv files found after recursive search.")
#                 print("  ℹ️ Proceeding without selecting .tsv files.")
#                 return True  # Allow script to continue

#             print(f"✅ Found {len(tsv_elements)} .tsv files. Selecting all...")
#             file_paths = []
#             selected_count = 0
#             for i, element in enumerate(tsv_elements):
#                 retries = max_retries
#                 while retries > 3:
#                     try:
#                         file_name = element.text.strip()
#                         tree_row = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')][1]")
#                         full_path = get_full_path(tree_row)
#                         print(f"  📁 Path for .tsv file {i + 1}/{len(tsv_elements)}: {full_path}")
#                         file_paths.append(full_path)
                        
#                         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#                         time.sleep(30)
#                         element.click()
#                         print(f"  ✅ Selected .tsv file {i + 1}/{len(tsv_elements)}: {file_name}")
#                         selected_count += 1
#                         time.sleep(30)
#                         break
#                     except (WebDriverException, StaleElementReferenceException) as e:
#                         retries -= 1
#                         file_name = element.text if element.text else "unknown file"
#                         print(f"  ⚠️ Could not process .tsv file {i + 1} ({file_name}) (Retry {max_retries - retries}/{max_retries}): {e}")
#                         if retries == 0:
#                             print(f"  ❌ Failed to process .tsv file {i + 1} ({file_name}) after {max_retries} retries.")
#                             file_paths.append(f"Error for file {file_name}: {str(e)}")
#                             break
#                         time.sleep(3)

#             if selected_count == 0:
#                 print("⚠️ No .tsv files were selected.")
#                 print("  ℹ️ Proceeding without selecting .tsv files.")
#                 return True  # Allow script to continue

#             try:
#                 with open("tsv_file_paths.txt", "w", encoding="utf-8") as f:
#                     for path in file_paths:
#                         f.write(f"{path}\n")
#                 print("✅ Saved .tsv file paths to 'tsv_file_paths.txt'.")
#             except Exception as e:
#                 print(f"❌ Error saving .tsv paths to file: {e}")

#             # Click "Metadata File" button after selecting .tsv files
#             print("🔄 Clicking 'Metadata File' button...")
#             retries = max_retries
#             while retries > 0:
#                 try:
#                     metadata_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Add Metadata File' and contains(., 'Metadata File')]")))
#                     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", metadata_btn)
#                     time.sleep(1)
#                     metadata_btn.click()
#                     print("✅ 'Metadata File' button clicked successfully.")
#                     time.sleep(1)
#                     return True
#                 except (WebDriverException, ElementClickInterceptedException) as e:
#                     retries -= 1
#                     print(f"  ⚠️ Failed to click 'Metadata File' button (Retry {max_retries - retries}/{max_retries}): {e}")
#                     if retries == 0:
#                         print("  ℹ️ Attempting JavaScript click fallback...")
#                         try:
#                             metadata_btn = driver.find_element(By.XPATH, "//button[@title='Add Metadata File' and contains(., 'Metadata File')]")
#                             driver.execute_script("arguments[0].click();", metadata_btn)
#                             print("✅ Fallback: 'Metadata File' button clicked via JavaScript.")
#                             time.sleep(1)
#                             return True
#                         except WebDriverException as js_e:
#                             print(f"  ❌ JavaScript fallback failed: {js_e}")
#                             print(f"  ℹ️ Proceeding without clicking 'Metadata File' button.")
#                             return True  # Allow script to continue
#                     time.sleep(3)

#         except WebDriverException as e:
#             print(f"❌ Error while selecting .tsv files on attempt {attempt}: {e}")
#             if attempt == max_attempts:
#                 print(f"  ℹ️ Proceeding without selecting .tsv files after {max_attempts} attempts.")
#                 return True  # Allow script to continue
#             attempt += 1
#             time.sleep(5)

# def configure_advanced_options(max_retries=3):
#     """Expand Advanced Network Options and Advanced Library Search Options, then set specific input values"""
#     try:
#         # Expand Advanced Network Options
#         print("🔄 Clicking 'Advanced Network Options' button to expand...")
#         retries = max_retries
#         while retries > 0:
#             try:
#                 advanced_network_btn = wait.until(EC.element_to_be_clickable((By.ID, "AdvancedNetworkOptions_showhide")))
#                 driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", advanced_network_btn)
#                 time.sleep(1)
#                 advanced_network_btn.click()
#                 print("✅ 'Advanced Network Options' button clicked to expand.")
#                 time.sleep(2)  # Wait for fields to appear
#                 break
#             except (WebDriverException, ElementClickInterceptedException) as e:
#                 retries -= 1
#                 print(f"  ⚠️ Failed to click 'Advanced Network Options' button (Retry {max_retries - retries}/{max_retries}): {e}")
#                 if retries == 0:
#                     print("  ❌ Failed to expand Advanced Network Options after retries.")
#                     return False
#                 time.sleep(3)

#         # Set "Min Pairs Cos" to 0.6
#         print("🔍 Searching for 'Min Pairs Cos' text...")
#         min_pairs_cos_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Min Pairs Cos')]]")))
#         print(f"✅ Found 'Min Pairs Cos' text at {min_pairs_cos_td.location}")
#         input_field = min_pairs_cos_td.find_element(By.XPATH, "./following-sibling::td//input[@name='PAIRS_MIN_COSINE']")
#         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
#         time.sleep(1)
#         input_field.clear()
#         input_field.send_keys("0.6")
#         print("✅ 'Min Pairs Cos' set to 0.6.")

#         # Set "Minimum Matched Fragment Ions" to 4
#         print("🔍 Searching for 'Minimum Matched Fragment Ions' text...")
#         min_ions_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Minimum Matched Fragment Ions')]]")))
#         print(f"✅ Found 'Minimum Matched Fragment Ions' text at {min_ions_td.location}")
#         input_field = min_ions_td.find_element(By.XPATH, "./following-sibling::td//input[@name='MIN_MATCHED_PEAKS']")
#         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
#         time.sleep(1)
#         input_field.clear()
#         input_field.send_keys("4")
#         print("✅ 'Minimum Matched Fragment Ions' set to 4.")

#         # Expand Advanced Library Search Options
#         print("🔄 Clicking 'Advanced Library Search Options' button to expand...")
#         retries = max_retries
#         while retries > 0:
#             try:
#                 advanced_library_btn = wait.until(EC.element_to_be_clickable((By.ID, "AdvancedLibrarySearchOptions_showhide")))
#                 driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", advanced_library_btn)
#                 time.sleep(1)
#                 advanced_library_btn.click()
#                 print("✅ 'Advanced Library Search Options' button clicked to expand.")
#                 time.sleep(2)  # Wait for fields to appear
#                 break
#             except (WebDriverException, ElementClickInterceptedException) as e:
#                 retries -= 1
#                 print(f"  ⚠️ Failed to click 'Advanced Library Search Options' button (Retry {max_retries - retries}/{max_retries}): {e}")
#                 if retries == 0:
#                     print("  ❌ Failed to expand Advanced Library Search Options after retries.")
#                     return False
#                 time.sleep(3)

#         # Set "Library Search Min Matched Peaks" to 4
#         print("🔍 Searching for 'Library Search Min Matched Peaks' text...")
#         lib_search_min_peaks_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Library Search Min Matched Peaks')]]")))
#         print(f"✅ Found 'Library Search Min Matched Peaks' text at {lib_search_min_peaks_td.location}")
#         input_field = lib_search_min_peaks_td.find_element(By.XPATH, "./following-sibling::td//input[@name='MIN_MATCHED_PEAKS_SEARCH']")
#         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
#         time.sleep(1)
#         input_field.clear()
#         input_field.send_keys("4")
#         print("✅ 'Library Search Min Matched Peaks' set to 4.")

#         # Set "Score Threshold" to 0.6
#         print("🔍 Searching for 'Score Threshold' text...")
#         score_threshold_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Score Threshold')]]")))
#         print(f"✅ Found 'Score Threshold' text at {score_threshold_td.location}")
#         input_field = score_threshold_td.find_element(By.XPATH, "./following-sibling::td//input[@name='SCORE_THRESHOLD']")
#         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
#         time.sleep(1)
#         input_field.clear()
#         input_field.send_keys("0.6")
#         print("✅ 'Score Threshold' set to 0.6.")

#         return True

#     except WebDriverException as e:
#         print(f"❌ Error configuring advanced options: {e}")
#         return False

# try:
#     # Step 1: Login
#     driver.get("https://gnps.ucsd.edu/ProteoSAFe/user/login.jsp")
#     wait.until(EC.presence_of_element_located((By.NAME, "user")))
#     driver.find_element(By.NAME, "user").clear()
#     driver.find_element(By.NAME, "password").clear()
#     driver.find_element(By.NAME, "user").send_keys(USERNAME)
#     driver.find_element(By.NAME, "password").send_keys(PASSWORD)
#     driver.find_element(By.NAME, "login").click()

#     # Step 2: Go to "Select Input Files" with retry and JavaScript fallback
#     print("🔄 Waiting for 'Select Input Files' button...")
#     wait.until(EC.presence_of_element_located((By.ID, "spec_on_server")))
#     time.sleep(5)  # Allow page to fully render
#     max_retries = 3
#     retries = max_retries
#     select_input_btn = None
#     while retries > 0:
#         try:
#             select_input_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Select Input Files']")))
#             driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_input_btn)
#             time.sleep(1)
#             select_input_btn.click()
#             print("✅ 'Select Input Files' button clicked successfully.")
#             break
#         except (ElementClickInterceptedException, WebDriverException) as e:
#             retries -= 1
#             print(f"  ⚠️ Failed to click 'Select Input Files' button (Retry {max_retries - retries}/{max_retries}): {e}")
#             if retries == 0:
#                 print("  ℹ️ Attempting JavaScript click fallback...")
#                 try:
#                     select_input_btn = driver.find_element(By.XPATH, "//input[@value='Select Input Files']")
#                     driver.execute_script("arguments[0].click();", select_input_btn)
#                     print("✅ Fallback: 'Select Input Files' button clicked via JavaScript.")
#                     break
#                 except WebDriverException as js_e:
#                     print(f"  ❌ JavaScript fallback failed: {js_e}")
#                     print(f"  ❌ Failed to click 'Select Input Files' button after {max_retries} retries and fallback.")
#                     raise
#             time.sleep(5)

#     # Step 3: Switch to new tab
#     wait.until(EC.number_of_windows_to_be(2))
#     driver.switch_to.window(driver.window_handles[-1])

#     # Step 4: Wait for dataset tree to appear
#     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dijitTreeRow")))
#     print("✅ Dataset tree loaded.")
#     time.sleep(30)  # Increased for tree rendering

#     # Step 5: Expand nodes selectively
#     expand_all_nodes()

#     # Step 6: Select all .mzXML files and collect their paths
#     if select_mzxml_files():
#         # Step 7: Click "Add Spectrum Files G1" button
#         print("🔄 Clicking 'Add Spectrum Files G1' button...")
#         add_spectrum_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Spectrum Files G1')]")))
#         add_spectrum_btn.click()
#         print("✅ 'Add Spectrum Files G1' button clicked.")

#         # Step 8: Expand folder containing USERNAME, select .tsv files, and click 'Metadata File' button
#         if select_tsv_files():
#             # Step 9: Click 'Finish Selection' button
#             print("🔄 Clicking 'Finish Selection' button...")
#             finish_selection_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Finish Selection')]")))
#             finish_selection_btn.click()
#             print("✅ 'Finish Selection' button clicked.")

#             # Step 10: Wait for the window to close and switch back to the original tab
#             wait.until(EC.number_of_windows_to_be(1))
#             driver.switch_to.window(driver.window_handles[0])
#             time.sleep(10)
#             print("✅ Switched back to the original tab.")

#             # Step 11: Configure advanced options
#             if configure_advanced_options():
#                 # Step 12: Set title to 'final_job'
#                 print("🔍 Setting title to 'final_job'...")
#                 title_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='desc' and @type='text']")))
#                 driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
#                 time.sleep(1)
#                 title_input.clear()
#                 title_input.send_keys("Aspergillus")
#                 print("✅ Title set to 'final_job'.")
#                 time.sleep(1)

#                 # Step 13: Click 'Submit' button with retry mechanism and JavaScript fallback
#                 print("🔄 Clicking 'Submit' button...")
#                 max_retries = 3
#                 retries = max_retries
#                 while retries > 0:
#                     try:
#                         submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit_workflow")))
#                         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
#                         time.sleep(1)
#                         submit_btn.click()
#                         print("✅ 'Submit' button clicked successfully.")
#                         time.sleep(30)
#                         break
#                     except WebDriverException as e:
#                         retries -= 1
#                         print(f"  ⚠️ Failed to click 'Submit' button (Retry {max_retries - retries}/{max_retries}): {e}")
#                         if retries == 0:
#                             print("  ℹ️ Attempting JavaScript fallback to submit form...")
#                             try:
#                                 driver.execute_script("ProteoSAFeInputUtils.submitInputForm();")
#                                 print("✅ Fallback: Form submitted via JavaScript.")
#                                 time.sleep(30)
#                                 break
#                             except WebDriverException as js_e:
#                                 print(f"  ❌ JavaScript fallback failed: {js_e}")
#                                 print(f"  ❌ Failed to submit form after {max_retries} retries and fallback.")
#                                 break
#                         time.sleep(5)
#             else:
#                 print("❌ Failed to configure advanced options. Proceeding with default settings.")
#         else:
#             print("❌ No .tsv files were selected. Skipping remaining steps.")
#     else:
#         print("❌ No .mzXML files were selected. Skipping remaining steps.")

# except Exception as e:
#     print("❌ ERROR:")
#     traceback.print_exc()

# finally:
#     print("✅ Script finished processing.")
#     driver.quit()

# import time
# import traceback
# import os
# import re
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, ElementClickInterceptedException

# def setup_driver():
#     """Configure and return a Chrome WebDriver instance"""
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--disable-extensions")
#     chrome_options.add_argument("--window-size=1920,1080")
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
#     driver = webdriver.Chrome(options=chrome_options)
#     return driver, WebDriverWait(driver, 90)

# def load_folder_names(file_path="cleaned_unique_paths.txt"):
#     """Load folder names from specified file into a set"""
#     folder_names = set()
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             for line in f:
#                 folder_name = line.strip()
#                 if folder_name:
#                     folder_names.add(folder_name)
#         print(f"✅ Loaded {len(folder_names)} folder names from {file_path}")
#         return folder_names
#     except Exception as e:
#         print(f"❌ Error loading {file_path}: {e}")
#         return set()

# def load_mzxml_filenames(file_path="mzxml_file_paths.txt"):
#     """Load mzXML filenames from specified file into a set"""
#     mzxml_filenames = set()
#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             for line in f:
#                 filename = line.strip()
#                 if filename and filename.endswith('.mzXML'):
#                     mzxml_filenames.add(filename)
#         print(f"✅ Loaded {len(mzxml_filenames)} mzXML filenames from {file_path}")
#         return mzxml_filenames
#     except Exception as e:
#         print(f"❌ Error loading {file_path}: {e}")
#         return set()

# def save_progress(node_index, file_path="expansion_progress.txt"):
#     """Save the last successfully expanded node index to a file"""
#     with open(file_path, "w") as f:
#         f.write(str(node_index))

# def load_progress(file_path="expansion_progress.txt"):
#     """Load the last successfully expanded node index from a file"""
#     if os.path.exists(file_path):
#         with open(file_path, "r") as f:
#             return int(f.read().strip())
#     return 0

# def login(driver, wait, username, password):
#     """Login to GNPS website"""
#     try:
#         driver.get("https://gnps.ucsd.edu/ProteoSAFe/user/login.jsp")
#         wait.until(EC.presence_of_element_located((By.NAME, "user")))
#         driver.find_element(By.NAME, "user").clear()
#         driver.find_element(By.NAME, "password").clear()
#         driver.find_element(By.NAME, "user").send_keys(username)
#         driver.find_element(By.NAME, "password").send_keys(password)
#         driver.find_element(By.NAME, "login").click()
#         print("✅ Logged in successfully")
#         return True
#     except Exception as e:
#         print(f"❌ Login failed: {e}")
#         return False

# def navigate_to_input_files(driver, wait, max_retries=3):
#     """Navigate to input files selection page"""
#     try:
#         print("🔄 Waiting for 'Select Input Files' button...")
#         wait.until(EC.presence_of_element_located((By.ID, "spec_on_server")))
#         time.sleep(5)
#         retries = max_retries
#         while retries > 0:
#             try:
#                 select_input_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Select Input Files']")))
#                 driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_input_btn)
#                 time.sleep(1)
#                 select_input_btn.click()
#                 print("✅ 'Select Input Files' button clicked")
#                 return True
#             except (ElementClickInterceptedException, WebDriverException) as e:
#                 retries -= 1
#                 print(f"  ⚠️ Failed to click 'Select Input Files' (Retry {max_retries - retries}/{max_retries}): {e}")
#                 if retries == 0:
#                     print("  ℹ️ Attempting JavaScript click...")
#                     try:
#                         select_input_btn = driver.find_element(By.XPATH, "//input[@value='Select Input Files']")
#                         driver.execute_script("arguments[0].click();", select_input_btn)
#                         print("✅ Fallback: 'Select Input Files' clicked via JavaScript")
#                         return True
#                     except WebDriverException as js_e:
#                         print(f"  ❌ JavaScript fallback failed: {js_e}")
#                         return False
#                 time.sleep(5)
#         return False
#     except Exception as e:
#         print(f"❌ Error navigating to input files: {e}")
#         return False

# def expand_all_nodes(driver, wait, folder_names, max_retries=3):
#     """Expand dataset nodes first, then folders listed in folder_names"""
#     last_successful_node = load_progress()
    
#     # Phase 1: Expand dataset nodes
#     iteration = 0
#     print("🔄 Phase 1: Expanding dataset nodes...")
#     while True:
#         try:
#             dataset_icons = driver.find_elements(By.XPATH, 
#                 "//span[contains(@class, 'dijitTreeLabel') and contains(text(), '[Dataset MSV00')]/ancestor::div[contains(@class, 'dijitTreeRow')]//img[contains(@class, 'dijitTreeExpandoClosed')]")
#             if not dataset_icons:
#                 print(f"✅ No more dataset nodes to expand after iteration {iteration + 1}")
#                 break
#             print(f"🔄 Iteration {iteration + 1}: Expanding {len(dataset_icons)} dataset nodes...")
#             for i, icon in enumerate(dataset_icons):
#                 node_index = last_successful_node + i + 1
#                 retries = max_retries
#                 while retries > 0:
#                     try:
#                         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
#                         time.sleep(0.7)
#                         label = icon.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')]//span[contains(@class, 'dijitTreeLabel')]").text.strip()
#                         icon.click()
#                         print(f"  ➕ Expanded dataset node {node_index}/{len(dataset_icons) + last_successful_node}: {label}")
#                         save_progress(node_index)
#                         time.sleep(0.7)
#                         break
#                     except (WebDriverException, StaleElementReferenceException) as e:
#                         retries -= 1
#                         print(f"  ⚠️ Could not expand dataset node {node_index} (Retry {max_retries - retries}/{max_retries}): {e}")
#                         if retries == 0:
#                             print(f"  ❌ Failed to expand dataset node {node_index}")
#                             continue
#                         time.sleep(3)
#             iteration += 1
#             last_successful_node += len(dataset_icons)
#             save_progress(last_successful_node)
#             time.sleep(3)
#         except WebDriverException as e:
#             print(f"❌ Error during dataset node expansion: {e}")
#             print("🔄 Attempting to recover...")
#             time.sleep(5)
#             continue

#     # Phase 2: Expand specified folders
#     iteration = 0
#     print("🔄 Phase 2: Expanding folders...")
#     while True:
# # .Bitdefender
#         try:
#             expand_icons = driver.find_elements(By.XPATH, "//img[contains(@class, 'dijitTreeExpandoClosed')]")
#             if not expand_icons:
#                 print(f"✅ No more folders to expand after iteration {iteration + 1}")
#                 break
#             print(f"🔄 Iteration {iteration + 1}: Checking {len(expand_icons)} unexpanded folders...")
#             nodes_expanded = 0
#             for i, icon in enumerate(expand_icons):
#                 node_index = last_successful_node + i + 1
#                 retries = max_retries
#                 while retries > 0:
#                     try:
#                         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
#                         time.sleep(0.7)
#                         label = icon.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')]//span[contains(@class, 'dijitTreeLabel')]").text.strip()
#                         if label in folder_names:
#                             icon.click()
#                             print(f"  ➕ Expanded folder {node_index}/{len(expand_icons) + last_successful_node}: {label}")
#                             save_progress(node_index)
#                             nodes_expanded += 1
#                             time.sleep(0.7)
#                             break
#                         else:
#                             print(f"  ℹ️ Skipped folder {node_index}/{len(expand_icons) + last_successful_node}: {label}")
#                             break
#                     except (WebDriverException, StaleElementReferenceException) as e:
#                         retries -= 1
#                         print(f"  ⚠️ Could not process folder {node_index} (Retry {max_retries - retries}/{max_retries}): {e}")
#                         if retries == 0:
#                             print(f"  ❌ Failed to process folder {node_index}")
#                             continue
#                         time.sleep(3)
#             if nodes_expanded == 0:
#                 print(f"✅ No matching folders expanded in iteration {iteration + 1}")
#                 break
#             iteration += 1
#             last_successful_node += len(expand_icons)
#             save_progress(last_successful_node)
#             time.sleep(3)
#         except WebDriverException as e:
#             print(f"❌ Error during folder expansion: {e}")
#             print("🔄 Attempting to recover...")
#             time.sleep(5)
#             continue

# def get_full_path(driver, element):
#     """Construct the full path by traversing up to the dataset root"""
#     path_parts = []
#     current = element
#     label = "unknown"
#     try:
#         label = current.find_element(By.XPATH, ".//span[contains(@class, 'dijitTreeLabel')]").text.strip()
#         if label:
#             path_parts.append(label)
#         max_depth = 50
#         depth = 0
#         dataset_id = None
#         while depth < max_depth:
#             try:
#                 parent = current.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')][1]")
#                 parent_label = parent.find_element(By.XPATH, ".//span[contains(@class, 'dijitTreeLabel')]").text.strip()
#                 if parent_label:
#                     match = re.match(r'^\[Dataset (MSV00.*?)\]', parent_label)
#                     if match:
#                         dataset_id = match.group(1)
#                         break
#                     path_parts.append(parent_label)
#                 try:
#                     parent.find_element(By.XPATH, ".//img[contains(@class, 'dijitTreeExpandoOpened')]")
#                     parent.find_element(By.XPATH, ".//span[contains(@class, 'dijitTreeContentExpanded')]")
#                 except WebDriverException:
#                     if dataset_id:
#                         break
#                     break
#                 current = parent
#                 depth += 1
#             except (WebDriverException, StaleElementReferenceException):
#                 break
#         if dataset_id:
#             path_parts.reverse()
#             full_path = f"{dataset_id}/{'/'.join(path_parts)}"
#         else:
#             full_path = "/".join(reversed(path_parts)) if path_parts else "Unknown path"
#         return full_path
#     except (WebDriverException, StaleElementReferenceException) as e:
#         print(f"  ⚠️ Error constructing path for '{label}': {e}")
#         return f"Error for file {label}: {str(e)}"

# def select_mzxml_files(driver, wait, mzxml_filenames, max_retries=3):
#     """Select .mzXML files listed in mzxml_filenames and save their paths"""
#     try:
#         print("🔍 Searching for .mzXML files...")
#         mzxml_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'dijitTreeLabel') and contains(text(), '.mzXML')]")
#         if not mzxml_elements:
#             print("⚠️ No .mzXML files found")
#             return False
#         if not mzxml_filenames:
#             print("⚠️ No filenames loaded from mzxml_file_paths.txt")
#             return False
#         print(f"✅ Found {len(mzxml_elements)} .mzXML files. Selecting listed files...")
#         file_paths = []
#         selected_count = 0
#         for i, element in enumerate(mzxml_elements):
#             try:
#                 file_name = element.text.strip()
#                 if file_name not in mzxml_filenames:
#                     print(f"  ℹ️ Skipped .mzXML file {i + 1}/{len(mzxml_elements)}: {file_name}")
#                     continue
#                 tree_row = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')][1]")
#                 full_path = get_full_path(driver, tree_row)
#                 print(f"  📁 Path for .mzXML file {i + 1}/{len(mzxml_elements)}: {full_path}")
#                 file_paths.append(full_path)
#                 driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#                 time.sleep(0.2)
#                 element.click()
#                 print(f"  ✅ Selected .mzXML file {i + 1}/{len(mzxml_elements)}: {file_name}")
#                 selected_count += 1
#                 time.sleep(0.2)
#             except (WebDriverException, StaleElementReferenceException) as e:
#                 file_name = element.text if element.text else "unknown file"
#                 print(f"  ⚠️ Could not process .mzXML file {i + 1} ({file_name}): {e}")
#                 file_paths.append(f"Error for file {file_name}: {str(e)}")
#         if selected_count == 0:
#             print("⚠️ No listed .mzXML files found")
#             return False
#         try:
#             with open("mzxml_file_paths.txt", "w", encoding="utf-8") as f:
#                 for path in file_paths:
#                     f.write(f"{path}\n")
#             print("✅ Saved .mzXML file paths")
#         except Exception as e:
#             print(f"❌ Error saving .mzXML paths: {e}")
#         return True
#     except WebDriverException as e:
#         print(f"❌ Error selecting .mzXML files: {e}")
#         return False

# def select_tsv_files(driver, wait, username, tsv_filename, max_retries=3, max_attempts=3):
#     """Find and expand folder containing username, select matching .tsv file, and click 'Metadata File'"""
#     attempt = 1
#     while attempt <= max_attempts:
#         try:
#             print(f"🔍 Attempt {attempt}/{max_attempts}: Searching for '{username}' folder...")
#             expand_icons = driver.find_elements(By.XPATH, 
#                 f"//span[contains(@class, 'dijitTreeLabel') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{username.lower()}')]/ancestor::div[contains(@class, 'dijitTreeRow')]//img[contains(@class, 'dijitTreeExpandoClosed')]")
#             folder_found = False
#             if expand_icons:
#                 print(f"✅ Found {len(expand_icons)} unexpanded '{username}' folder(s)")
#                 for i, icon in enumerate(expand_icons):
#                     retries = max_retries
#                     while retries > 0:
#                         try:
#                             driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
#                             time.sleep(0.7)
#                             label = icon.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')]//span[contains(@class, 'dijitTreeLabel')]").text.strip()
#                             icon.click()
#                             print(f"  ➕ Expanded folder {i + 1}/{len(expand_icons)}: {label}")
#                             folder_found = True
#                             time.sleep(15)
#                             break
#                         except (WebDriverException, StaleElementReferenceException) as e:
#                             retries -= 1
#                             print(f"  ⚠️ Could not expand '{label}' (Retry {max_retries - retries}/{max_retries}): {e}")
#                             if retries == 0:
#                                 print(f"  ❌ Failed to expand '{label}'")
#                                 continue
#                             time.sleep(15)
#                     if folder_found:
#                         break
#             else:
#                 folder_elements = driver.find_elements(By.XPATH, 
#                     f"//span[contains(@class, 'dijitTreeLabel') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{username.lower()}')]")
#                 if folder_elements:
#                     print(f"  ℹ️ '{username}' folder already expanded")
#                     folder_found = True
#                 else:
#                     print(f"⚠️ No '{username}' folder found on attempt {attempt}")
#                     if attempt == max_attempts:
#                         print(f"  ℹ️ Proceeding without selecting .tsv file")
#                         return True
#                     attempt += 1
#                     time.sleep(10)
#                     continue

#             if not folder_found:
#                 print(f"❌ Could not find '{username}' folder on attempt {attempt}")
#                 if attempt == max_attempts:
#                     print(f"  ℹ️ Proceeding without selecting .tsv file")
#                     return True
#                 attempt += 1
#                 time.sleep(5)
#                 continue

#             print(f"🔍 Searching for .tsv file: {tsv_filename}")
#             tsv_elements = []
#             def find_tsv_elements(element):
#                 try:
#                     if element.tag_name == "span" and "dijitTreeLabel" in element.get_attribute("class"):
#                         text = element.text.strip()
#                         if text == tsv_filename:
#                             tsv_elements.append(element)
#                             print(f"  📍 Found matching .tsv file: {text}")
#                     children = element.find_elements(By.XPATH, "./*")
#                     for child in children:
#                         find_tsv_elements(child)
#                 except WebDriverException as e:
#                     print(f"  ⚠️ Error traversing DOM: {e}")

#             expanded_folder = driver.find_element(By.XPATH, f"//span[contains(@class, 'dijitTreeLabel') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{username.lower()}')]/ancestor::div[contains(@class, 'dijitTreeRow')]")
#             container = expanded_folder.find_element(By.XPATH, "./following-sibling::div[contains(@class, 'dijitTreeContainer')]")
#             find_tsv_elements(container)

#             if not tsv_elements:
#                 print(f"⚠️ No .tsv file named {tsv_filename} found")
#                 return True

#             print(f"✅ Found {len(tsv_elements)} matching .tsv file(s)")
#             file_paths = []
#             selected_count = 0
#             for i, element in enumerate(tsv_elements):
#                 retries = max_retries
#                 while retries > 0:
#                     try:
#                         file_name = element.text.strip()
#                         tree_row = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')][1]")
#                         full_path = get_full_path(driver, tree_row)
#                         print(f"  📁 Path for .tsv file {i + 1}/{len(tsv_elements)}: {full_path}")
#                         file_paths.append(full_path)
#                         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
#                         time.sleep(0.7)
#                         element.click()
#                         print(f"  ✅ Selected .tsv file {i + 1}/{len(tsv_elements)}: {file_name}")
#                         selected_count += 1
#                         time.sleep(0.7)
#                         break
#                     except (WebDriverException, StaleElementReferenceException) as e:
#                         retries -= 1
#                         file_name = element.text if element.text else "unknown file"
#                         print(f"  ⚠️ Could not process .tsv file {i + 1} ({file_name}) (Retry {max_retries - retries}/{max_retries}): {e}")
#                         if retries == 0:
#                             print(f"  ❌ Failed to process .tsv file {i + 1} ({file_name})")
#                             file_paths.append(f"Error for file {file_name}: {str(e)}")
#                             break
#                         time.sleep(3)

#             if selected_count == 0:
#                 print("⚠️ No .tsv files were selected")
#                 return True

#             try:
#                 with open("tsv_file_paths.txt", "w", encoding="utf-8") as f:
#                     for path in file_paths:
#                         f.write(f"{path}\n")
#                 print("✅ Saved .tsv file paths")
#             except Exception as e:
#                 print(f"❌ Error saving .tsv paths: {e}")

#             print("🔄 Clicking 'Metadata File' button...")
#             retries = max_retries
#             while retries > 0:
#                 try:
#                     metadata_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Add Metadata File' and contains(., 'Metadata File')]")))
#                     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", metadata_btn)
#                     time.sleep(1)
#                     metadata_btn.click()
#                     print("✅ 'Metadata File' button clicked")
#                     return True
#                 except (WebDriverException, ElementClickInterceptedException) as e:
#                     retries -= 1
#                     print(f"  ⚠️ Failed to click 'Metadata File' (Retry {max_retries - retries}/{max_retries}): {e}")
#                     if retries == 0:
#                         print("  ℹ️ Attempting JavaScript click...")
#                         try:
#                             metadata_btn = driver.find_element(By.XPATH, "//button[@title='Add Metadata File' and contains(., 'Metadata File')]")
#                             driver.execute_script("arguments[0].click();", metadata_btn)
#                             print("✅ Fallback: 'Metadata File' clicked via JavaScript")
#                             return True
#                         except WebDriverException as js_e:
#                             print(f"  ❌ JavaScript fallback failed: {js_e}")
#                             return True
#                     time.sleep(3)
#         except WebDriverException as e:
#             print(f"❌ Error selecting .tsv files on attempt {attempt}: {e}")
#             attempt += 1
#             time.sleep(5)
#     return True

# def configure_advanced_options(driver, wait, max_retries=3):
#     """Configure advanced network and library search options"""
#     try:
#         print("🔄 Clicking 'Advanced Network Options'...")
#         retries = max_retries
#         while retries > 0:
#             try:
#                 advanced_network_btn = wait.until(EC.element_to_be_clickable((By.ID, "AdvancedNetworkOptions_showhide")))
#                 driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", advanced_network_btn)
#                 time.sleep(1)
#                 advanced_network_btn.click()
#                 print("✅ 'Advanced Network Options' expanded")
#                 break
#             except (WebDriverException, ElementClickInterceptedException) as e:
#                 retries -= 1
#                 print(f"  ⚠️ Failed to click 'Advanced Network Options' (Retry {max_retries - retries}/{max_retries}): {e}")
#                 if retries == 0:
#                     print("  ❌ Failed to expand Advanced Network Options")
#                     return False
#                 time.sleep(3)

#         print("🔍 Setting 'Min Pairs Cos' to 0.6...")
#         min_pairs_cos_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Min Pairs Cos')]]")))
#         input_field = min_pairs_cos_td.find_element(By.XPATH, "./following-sibling::td//input[@name='PAIRS_MIN_COSINE']")
#         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
#         time.sleep(1)
#         input_field.clear()
#         input_field.send_keys("0.6")
#         print("✅ 'Min Pairs Cos' set to 0.6")

#         print("🔍 Setting 'Minimum Matched Fragment Ions' to 4...")
#         min_ions_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Minimum Matched Fragment Ions')]]")))
#         input_field = min_ions_td.find_element(By.XPATH, "./following-sibling::td//input[@name='MIN_MATCHED_PEAKS']")
#         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
#         time.sleep(1)
#         input_field.clear()
#         input_field.send_keys("4")
#         print("✅ 'Minimum Matched Fragment Ions' set to 4")

#         print("🔄 Clicking 'Advanced Library Search Options'...")
#         retries = max_retries
#         while retries > 0:
#             try:
#                 advanced_library_btn = wait.until(EC.element_to_be_clickable((By.ID, "AdvancedLibrarySearchOptions_showhide")))
#                 driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", advanced_library_btn)
#                 time.sleep(1)
#                 advanced_library_btn.click()
#                 print("✅ 'Advanced Library Search Options' expanded")
#                 break
#             except (WebDriverException, ElementClickInterceptedException) as e:
#                 retries -= 1
#                 print(f"  ⚠️ Failed to click 'Advanced Library Search Options' (Retry {max_retries - retries}/{max_retries}): {e}")
#                 if retries == 0:
#                     print("  ❌ Failed to expand Advanced Library Search Options")
#                     return False
#                 time.sleep(3)

#         print("🔍 Setting 'Library Search Min Matched Peaks' to 4...")
#         lib_search_min_peaks_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Library Search Min Matched Peaks')]]")))
#         input_field = lib_search_min_peaks_td.find_element(By.XPATH, "./following-sibling::td//input[@name='MIN_MATCHED_PEAKS_SEARCH']")
#         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
#         time.sleep(1)
#         input_field.clear()
#         input_field.send_keys("4")
#         print("✅ 'Library Search Min Matched Peaks' set to 4")

#         print("🔍 Setting 'Score Threshold' to 0.6...")
#         score_threshold_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Score Threshold')]]")))
#         input_field = score_threshold_td.find_element(By.XPATH, "./following-sibling::td//input[@name='SCORE_THRESHOLD']")
#         driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
#         time.sleep(1)
#         input_field.clear()
#         input_field.send_keys("0.6")
#         print("✅ 'Score Threshold' set to 0.6")

#         return True
#     except WebDriverException as e:
#         print(f"❌ Error configuring advanced options: {e}")
#         return False

# def run_gnps_workflow(username, password, tsv_filename, job_title="Aspergillus"):
#     """Main function to run the GNPS automation workflow"""
#     driver, wait = setup_driver()
#     folder_names = load_folder_names()
#     mzxml_filenames = load_mzxml_filenames()
    
#     try:
#         if not login(driver, wait, username, password):
#             return False

#         if not navigate_to_input_files(driver, wait):
#             return False

#         wait.until(EC.number_of_windows_to_be(2))
#         driver.switch_to.window(driver.window_handles[-1])
#         wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dijitTreeRow")))
#         print("✅ Dataset tree loaded")
#         time.sleep(30)

#         expand_all_nodes(driver, wait, folder_names)

#         if select_mzxml_files(driver, wait, mzxml_filenames):
#             print("🔄 Clicking 'Add Spectrum Files G1'...")
#             add_spectrum_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Spectrum Files G1')]")))
#             add_spectrum_btn.click()
#             print("✅ 'Add Spectrum Files G1' clicked")

#             if select_tsv_files(driver, wait, username, tsv_filename):
#                 print("🔄 Clicking 'Finish Selection'...")
#                 finish_selection_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Finish Selection')]")))
#                 finish_selection_btn.click()
#                 print("✅ 'Finish Selection' clicked")

#                 wait.until(EC.number_of_windows_to_be(1))
#                 driver.switch_to.window(driver.window_handles[0])
#                 time.sleep(10)
#                 print("✅ Switched back to original tab")

#                 if configure_advanced_options(driver, wait):
#                     print(f"🔍 Setting title to '{job_title}'...")
#                     title_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='desc' and @type='text']")))
#                     driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
#                     time.sleep(1)
#                     title_input.clear()
#                     title_input.send_keys(job_title)
#                     print(f"✅ Title set to '{job_title}'")

#                     print("🔄 Clicking 'Submit'...")
#                     max_retries = 3
#                     retries = max_retries
#                     while retries > 0:
#                         try:
#                             submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit_workflow")))
#                             driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
#                             time.sleep(1)
#                             submit_btn.click()
#                             print("✅ 'Submit' clicked")
#                             time.sleep(30)
#                             return True
#                         except WebDriverException as e:
#                             retries -= 1
#                             print(f"  ⚠️ Failed to click 'Submit' (Retry {max_retries - retries}/{max_retries}): {e}")
#                             if retries == 0:
#                                 print("  ℹ️ Attempting JavaScript submit...")
#                                 try:
#                                     driver.execute_script("ProteoSAFeInputUtils.submitInputForm();")
#                                     print("✅ Fallback: Form submitted via JavaScript")
#                                     time.sleep(30)
#                                     return True
#                                 except WebDriverException as js_e:
#                                     print(f"  ❌ JavaScript fallback failed: {js_e}")
#                                     return False
#                             time.sleep(5)
#                 else:
#                     print("❌ Failed to configure advanced options")
#             else:
#                 print(f"❌ No .tsv file named {tsv_filename} selected")
#         else:
#             print("❌ No .mzXML files selected")
#         return False
#     except Exception as e:
#         print(f"❌ ERROR: {e}")
#         traceback.print_exc()
#         return False
#     finally:
#         print("✅ Script finished")
#         driver.quit()

# if __name__ == "__main__":
#     run_gnps_workflow("jibanp", "1234567890", "Bacillus_specific_metadata.tsv", "Aspergillus")



import time
import traceback
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException, ElementClickInterceptedException

def setup_driver():
    """Configure and return a Chrome WebDriver instance"""
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=chrome_options)
    return driver, WebDriverWait(driver, 90)

def load_folder_names(file_path="cleaned_unique_paths.txt"):
    """Load folder names from specified file into a set"""
    folder_names = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                folder_name = line.strip()
                if folder_name:
                    folder_names.add(folder_name)
        print(f"Loaded {len(folder_names)} folder names from {file_path}")
        return folder_names
    except Exception as e:
        print(f" Error loading {file_path}: {e}")
        return set()

def load_filenames(file_path="mzxml_file_paths.txt"):
    """Load filenames from specified file into a set"""
    filenames = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                filename = line.strip()
                if filename:
                    filenames.add(filename)
        print(f" Loaded {len(filenames)} filenames from {file_path}")
        return filenames
    except Exception as e:
        print(f" Error loading {file_path}: {e}")
        return set()

def save_progress(node_index, file_path="expansion_progress.txt"):
    """Save the last successfully expanded node index to a file"""
    with open(file_path, "w") as f:
        f.write(str(node_index))

def load_progress(file_path="expansion_progress.txt"):
    """Load the last successfully expanded node index from a file"""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return int(f.read().strip())
    return 0

def login(driver, wait, username, password):
    """Login to GNPS website"""
    try:
        driver.get("https://gnps.ucsd.edu/ProteoSAFe/user/login.jsp")
        wait.until(EC.presence_of_element_located((By.NAME, "user")))
        driver.find_element(By.NAME, "user").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.NAME, "user").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "login").click()
        print(" Logged in successfully")
        return True
    except Exception as e:
        print(f" Login failed: {e}")
        return False

def navigate_to_input_files(driver, wait, max_retries=3):
    """Navigate to input files selection page"""
    try:
        print(" Waiting for 'Select Input Files' button...")
        wait.until(EC.presence_of_element_located((By.ID, "spec_on_server")))
        time.sleep(5)
        retries = max_retries
        while retries > 0:
            try:
                select_input_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Select Input Files']")))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", select_input_btn)
                time.sleep(1)
                select_input_btn.click()
                print(" 'Select Input Files' button clicked")
                return True
            except (ElementClickInterceptedException, WebDriverException) as e:
                retries -= 1
                print(f"   Failed to click 'Select Input Files' (Retry {max_retries - retries}/{max_retries}): {e}")
                if retries == 0:
                    print("  Attempting JavaScript click...")
                    try:
                        select_input_btn = driver.find_element(By.XPATH, "//input[@value='Select Input Files']")
                        driver.execute_script("arguments[0].click();", select_input_btn)
                        print(" Fallback: 'Select Input Files' clicked via JavaScript")
                        return True
                    except WebDriverException as js_e:
                        print(f"   JavaScript fallback failed: {js_e}")
                        return False
                time.sleep(5)
        return False
    except Exception as e:
        print(f" Error navigating to input files: {e}")
        return False

def expand_all_nodes(driver, wait, folder_names, max_retries=3):
    """Expand dataset nodes first, then folders listed in folder_names"""
    last_successful_node = load_progress()
    
    # Phase 1: Expand dataset nodes
    iteration = 0
    print(" Phase 1: Expanding dataset nodes...")
    while True:
        try:
            dataset_icons = driver.find_elements(By.XPATH, 
                "//span[contains(@class, 'dijitTreeLabel') and contains(text(), '[Dataset MSV00')]/ancestor::div[contains(@class, 'dijitTreeRow')]//img[contains(@class, 'dijitTreeExpandoClosed')]")
            if not dataset_icons:
                print(f" No more dataset nodes to expand after iteration {iteration + 1}")
                break
            print(f" Iteration {iteration + 1}: Expanding {len(dataset_icons)} dataset nodes...")
            for i, icon in enumerate(dataset_icons):
                node_index = last_successful_node + i + 1
                retries = max_retries
                while retries > 0:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
                        time.sleep(0.7)
                        label = icon.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')]//span[contains(@class, 'dijitTreeLabel')]").text.strip()
                        icon.click()
                        print(f"  Expanded dataset node {node_index}/{len(dataset_icons) + last_successful_node}: {label}")
                        save_progress(node_index)
                        time.sleep(0.7)
                        break
                    except (WebDriverException, StaleElementReferenceException) as e:
                        retries -= 1
                        print(f"   Could not expand dataset node {node_index} (Retry {max_retries - retries}/{max_retries}): {e}")
                        if retries == 0:
                            print(f"   Failed to expand dataset node {node_index}")
                            continue
                        time.sleep(3)
            iteration += 1
            last_successful_node += len(dataset_icons)
            save_progress(last_successful_node)
            time.sleep(3)
        except WebDriverException as e:
            print(f" Error during dataset node expansion: {e}")
            print(" Attempting to recover...")
            time.sleep(5)
            continue

    # Phase 2: Expand specified folders
    iteration = 0
    print("🔄 Phase 2: Expanding folders...")
    while True:
        try:
            expand_icons = driver.find_elements(By.XPATH, "//img[contains(@class, 'dijitTreeExpandoClosed')]")
            if not expand_icons:
                print(f" No more folders to expand after iteration {iteration + 1}")
                break
            print(f" Iteration {iteration + 1}: Checking {len(expand_icons)} unexpanded folders...")
            nodes_expanded = 0
            for i, icon in enumerate(expand_icons):
                node_index = last_successful_node + i + 1
                retries = max_retries
                while retries > 0:
                    try:
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
                        time.sleep(0.7)
                        label = icon.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')]//span[contains(@class, 'dijitTreeLabel')]").text.strip()
                        if label in folder_names:
                            icon.click()
                            print(f"   Expanded folder {node_index}/{len(expand_icons) + last_successful_node}: {label}")
                            save_progress(node_index)
                            nodes_expanded += 1
                            time.sleep(0.7)
                            break
                        else:
                            print(f"   Skipped folder {node_index}/{len(expand_icons) + last_successful_node}: {label}")
                            break
                    except (WebDriverException, StaleElementReferenceException) as e:
                        retries -= 1
                        print(f"   Could not process folder {node_index} (Retry {max_retries - retries}/{max_retries}): {e}")
                        if retries == 0:
                            print(f"   Failed to process folder {node_index}")
                            continue
                        time.sleep(3)
            if nodes_expanded == 0:
                print(f" No matching folders expanded in iteration {iteration + 1}")
                break
            iteration += 1
            last_successful_node += len(expand_icons)
            save_progress(last_successful_node)
            time.sleep(3)
        except WebDriverException as e:
            print(f" Error during folder expansion: {e}")
            print(" Attempting to recover...")
            time.sleep(5)
            continue

def get_full_path(driver, element):
    """Construct the full path by traversing up to the dataset root"""
    path_parts = []
    current = element
    label = "unknown"
    try:
        label = current.find_element(By.XPATH, ".//span[contains(@class, 'dijitTreeLabel')]").text.strip()
        if label:
            path_parts.append(label)
        max_depth = 50
        depth = 0
        dataset_id = None
        while depth < max_depth:
            try:
                parent = current.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')][1]")
                parent_label = parent.find_element(By.XPATH, ".//span[contains(@class, 'dijitTreeLabel')]").text.strip()
                if parent_label:
                    match = re.match(r'^\[Dataset (MSV00.*?)\]', parent_label)
                    if match:
                        dataset_id = match.group(1)
                        break
                    path_parts.append(parent_label)
                try:
                    parent.find_element(By.XPATH, ".//img[contains(@class, 'dijitTreeExpandoOpened')]")
                    parent.find_element(By.XPATH, ".//span[contains(@class, 'dijitTreeContentExpanded')]")
                except WebDriverException:
                    if dataset_id:
                        break
                    break
                current = parent
                depth += 1
            except (WebDriverException, StaleElementReferenceException):
                break
        if dataset_id:
            path_parts.reverse()
            full_path = f"{dataset_id}/{'/'.join(path_parts)}"
        else:
            full_path = "/".join(reversed(path_parts)) if path_parts else "Unknown path"
        return full_path
    except (WebDriverException, StaleElementReferenceException) as e:
        print(f"   Error constructing path for '{label}': {e}")
        return f"Error for file {label}: {str(e)}"

def select_files(driver, wait, filenames, max_retries=3):
    """Select files listed in filenames and save their paths"""
    try:
        print(" Searching for listed files...")
        file_elements = driver.find_elements(By.XPATH, "//span[contains(@class, 'dijitTreeLabel')]")
        if not file_elements:
            print(" No files found")
            return False
        if not filenames:
            print(" No filenames loaded from mzxml_file_paths.txt")
            return False
        print(f" Found {len(file_elements)} files. Selecting listed files...")
        file_paths = []
        selected_count = 0
        for i, element in enumerate(file_elements):
            try:
                file_name = element.text.strip()
                if file_name not in filenames:
                    print(f"   Skipped file {i + 1}/{len(file_elements)}: {file_name}")
                    continue
                tree_row = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')][1]")
                full_path = get_full_path(driver, tree_row)
                print(f"   Path for file {i + 1}/{len(file_elements)}: {full_path}")
                file_paths.append(full_path)
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                time.sleep(0.2)
                element.click()
                print(f"   Selected file {i + 1}/{len(file_elements)}: {file_name}")
                selected_count += 1
                time.sleep(0.2)
            except (WebDriverException, StaleElementReferenceException) as e:
                file_name = element.text if element.text else "unknown file"
                print(f"   Could not process file {i + 1} ({file_name}): {e}")
                file_paths.append(f"Error for file {file_name}: {str(e)}")
        if selected_count == 0:
            print(" No listed files found")
            return False
        try:
            with open("selected_file_paths.txt", "w", encoding="utf-8") as f:
                for path in file_paths:
                    f.write(f"{path}\n")
            print(" Saved selected file paths")
        except Exception as e:
            print(f" Error saving file paths: {e}")
        return True
    except WebDriverException as e:
        print(f" Error selecting files: {e}")
        return False

def select_tsv_files(driver, wait, username, tsv_filename, max_retries=3, max_attempts=3):
    """Find and expand folder containing username, select matching .tsv file, and click 'Metadata File'"""
    attempt = 1
    while attempt <= max_attempts:
        try:
            print(f" Attempt {attempt}/{max_attempts}: Searching for '{username}' folder...")
            expand_icons = driver.find_elements(By.XPATH, 
                f"//span[contains(@class, 'dijitTreeLabel') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{username.lower()}')]/ancestor::div[contains(@class, 'dijitTreeRow')]//img[contains(@class, 'dijitTreeExpandoClosed')]")
            folder_found = False
            if expand_icons:
                print(f" Found {len(expand_icons)} unexpanded '{username}' folder(s)")
                for i, icon in enumerate(expand_icons):
                    retries = max_retries
                    while retries > 0:
                        try:
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", icon)
                            time.sleep(0.7)
                            label = icon.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')]//span[contains(@class, 'dijitTreeLabel')]").text.strip()
                            icon.click()
                            print(f"  ➕ Expanded folder {i + 1}/{len(expand_icons)}: {label}")
                            folder_found = True
                            time.sleep(60)
                            break
                        except (WebDriverException, StaleElementReferenceException) as e:
                            retries -= 1
                            print(f"   Could not expand '{label}' (Retry {max_retries - retries}/{max_retries}): {e}")
                            if retries == 0:
                                print(f"   Failed to expand '{label}'")
                                continue
                            time.sleep(15)
                    if folder_found:
                        break
            else:
                folder_elements = driver.find_elements(By.XPATH, 
                    f"//span[contains(@class, 'dijitTreeLabel') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{username.lower()}')]")
                if folder_elements:
                    print(f"   '{username}' folder already expanded")
                    folder_found = True
                else:
                    print(f" No '{username}' folder found on attempt {attempt}")
                    if attempt == max_attempts:
                        print(f"   Proceeding without selecting .tsv file")
                        return True
                    attempt += 1
                    time.sleep(10)
                    continue

            if not folder_found:
                print(f" Could not find '{username}' folder on attempt {attempt}")
                if attempt == max_attempts:
                    print(f"   Proceeding without selecting .tsv file")
                    return True
                attempt += 1
                time.sleep(60)
                continue

            print(f" Searching for .tsv file: {tsv_filename}")
            tsv_elements = []
            def find_tsv_elements(element):
                try:
                    if element.tag_name == "span" and "dijitTreeLabel" in element.get_attribute("class"):
                        text = element.text.strip()
                        if text == tsv_filename:
                            tsv_elements.append(element)
                            print(f"   Found matching .tsv file: {text}")
                    children = element.find_elements(By.XPATH, "./*")
                    for child in children:
                        find_tsv_elements(child)
                except WebDriverException as e:
                    print(f"   Error traversing DOM: {e}")

            expanded_folder = driver.find_element(By.XPATH, f"//span[contains(@class, 'dijitTreeLabel') and contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{username.lower()}')]/ancestor::div[contains(@class, 'dijitTreeRow')]")
            container = expanded_folder.find_element(By.XPATH, "./following-sibling::div[contains(@class, 'dijitTreeContainer')]")
            find_tsv_elements(container)

            if not tsv_elements:
                print(f" No .tsv file named {tsv_filename} found")
                return True

            print(f" Found {len(tsv_elements)} matching .tsv file(s)")
            file_paths = []
            selected_count = 0
            for i, element in enumerate(tsv_elements):
                retries = max_retries
                while retries > 0:
                    try:
                        file_name = element.text.strip()
                        tree_row = element.find_element(By.XPATH, "./ancestor::div[contains(@class, 'dijitTreeRow')][1]")
                        full_path = get_full_path(driver, tree_row)
                        print(f"   Path for .tsv file {i + 1}/{len(tsv_elements)}: {full_path}")
                        file_paths.append(full_path)
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                        time.sleep(1.7)
                        element.click()
                        print(f"   Selected .tsv file {i + 1}/{len(tsv_elements)}: {file_name}")
                        selected_count += 1
                        time.sleep(1.7)
                        break
                    except (WebDriverException, StaleElementReferenceException) as e:
                        retries -= 1
                        file_name = element.text if element.text else "unknown file"
                        print(f"   Could not process .tsv file {i + 1} ({file_name}) (Retry {max_retries - retries}/{max_retries}): {e}")
                        if retries == 0:
                            print(f"   Failed to process .tsv file {i + 1} ({file_name})")
                            file_paths.append(f"Error for file {file_name}: {str(e)}")
                            break
                        time.sleep(3)

            if selected_count == 0:
                print(" No .tsv files were selected")
                return True

            try:
                with open("tsv_file_paths.txt", "w", encoding="utf-8") as f:
                    for path in file_paths:
                        f.write(f"{path}\n")
                print(" Saved .tsv file paths")
            except Exception as e:
                print(f" Error saving .tsv paths: {e}")

            print(" Clicking 'Metadata File' button...")
            retries = max_retries
            while retries > 0:
                try:
                    metadata_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Add Metadata File' and contains(., 'Metadata File')]")))
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", metadata_btn)
                    time.sleep(1)
                    metadata_btn.click()
                    print(" 'Metadata File' button clicked")
                    return True
                except (WebDriverException, ElementClickInterceptedException) as e:
                    retries -= 1
                    print(f"   Failed to click 'Metadata File' (Retry {max_retries - retries}/{max_retries}): {e}")
                    if retries == 0:
                        print("   Attempting JavaScript click...")
                        try:
                            metadata_btn = driver.find_element(By.XPATH, "//button[@title='Add Metadata File' and contains(., 'Metadata File')]")
                            driver.execute_script("arguments[0].click();", metadata_btn)
                            print(" Fallback: 'Metadata File' clicked via JavaScript")
                            return True
                        except WebDriverException as js_e:
                            print(f"   JavaScript fallback failed: {js_e}")
                            return True
                    time.sleep(3)
        except WebDriverException as e:
            print(f" Error selecting .tsv files on attempt {attempt}: {e}")
            attempt += 1
            time.sleep(5)
    return True

def configure_advanced_options(driver, wait, max_retries=3):
    """Configure advanced network and library search options"""
    try:
        print(" Clicking 'Advanced Network Options'...")
        retries = max_retries
        while retries > 0:
            try:
                advanced_network_btn = wait.until(EC.element_to_be_clickable((By.ID, "AdvancedNetworkOptions_showhide")))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", advanced_network_btn)
                time.sleep(1)
                advanced_network_btn.click()
                print(" 'Advanced Network Options' expanded")
                break
            except (WebDriverException, ElementClickInterceptedException) as e:
                retries -= 1
                print(f" Failed to click 'Advanced Network Options' (Retry {max_retries - retries}/{max_retries}): {e}")
                if retries == 0:
                    print("   Failed to expand Advanced Network Options")
                    return False
                time.sleep(3)

        print("🔍 Setting 'Min Pairs Cos' to 0.6...")
        min_pairs_cos_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Min Pairs Cos')]]")))
        input_field = min_pairs_cos_td.find_element(By.XPATH, "./following-sibling::td//input[@name='PAIRS_MIN_COSINE']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
        time.sleep(1)
        input_field.clear()
        input_field.send_keys("0.6")
        print(" 'Min Pairs Cos' set to 0.6")

        print(" Setting 'Minimum Matched Fragment Ions' to 4...")
        min_ions_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Minimum Matched Fragment Ions')]]")))
        input_field = min_ions_td.find_element(By.XPATH, "./following-sibling::td//input[@name='MIN_MATCHED_PEAKS']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
        time.sleep(1)
        input_field.clear()
        input_field.send_keys("4")
        print(" 'Minimum Matched Fragment Ions' set to 4")

        print(" Clicking 'Advanced Library Search Options'...")
        retries = max_retries
        while retries > 0:
            try:
                advanced_library_btn = wait.until(EC.element_to_be_clickable((By.ID, "AdvancedLibrarySearchOptions_showhide")))
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", advanced_library_btn)
                time.sleep(1)
                advanced_library_btn.click()
                print(" 'Advanced Library Search Options' expanded")
                break
            except (WebDriverException, ElementClickInterceptedException) as e:
                retries -= 1
                print(f"   Failed to click 'Advanced Library Search Options' (Retry {max_retries - retries}/{max_retries}): {e}")
                if retries == 0:
                    print("   Failed to expand Advanced Library Search Options")
                    return False
                time.sleep(3)

        print(" Setting 'Library Search Min Matched Peaks' to 4...")
        lib_search_min_peaks_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Library Search Min Matched Peaks')]]")))
        input_field = lib_search_min_peaks_td.find_element(By.XPATH, "./following-sibling::td//input[@name='MIN_MATCHED_PEAKS_SEARCH']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
        time.sleep(1)
        input_field.clear()
        input_field.send_keys("4")
        print(" 'Library Search Min Matched Peaks' set to 4")

        print(" Setting 'Score Threshold' to 0.6...")
        score_threshold_td = wait.until(EC.presence_of_element_located((By.XPATH, "//td[span[contains(@class, 'help') and contains(text(), 'Score Threshold')]]")))
        input_field = score_threshold_td.find_element(By.XPATH, "./following-sibling::td//input[@name='SCORE_THRESHOLD']")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
        time.sleep(1)
        input_field.clear()
        input_field.send_keys("0.6")
        print(" 'Score Threshold' set to 0.6")

        return True
    except WebDriverException as e:
        print(f" Error configuring advanced options: {e}")
        return False

def run_gnps_workflow(username, password, tsv_filename, job_title="Aspergillus"):
    """Main function to run the GNPS automation workflow"""
    driver, wait = setup_driver()
    folder_names = load_folder_names()
    filenames = load_filenames()
    
    try:
        if not login(driver, wait, username, password):
            return False

        if not navigate_to_input_files(driver, wait):
            return False

        wait.until(EC.number_of_windows_to_be(2))
        driver.switch_to.window(driver.window_handles[-1])
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dijitTreeRow")))
        print(" Dataset tree loaded")
        time.sleep(30)

        expand_all_nodes(driver, wait, folder_names)

        if select_files(driver, wait, filenames):
            print(" Clicking 'Add Spectrum Files G1'...")
            add_spectrum_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Spectrum Files G1')]")))
            add_spectrum_btn.click()
            print(" 'Add Spectrum Files G1' clicked")

            if select_tsv_files(driver, wait, username, tsv_filename):
                print(" Clicking 'Finish Selection'...")
                finish_selection_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Finish Selection')]")))
                finish_selection_btn.click()
                print(" 'Finish Selection' clicked")

                wait.until(EC.number_of_windows_to_be(1))
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(10)
                print(" Switched back to original tab")

                if configure_advanced_options(driver, wait):
                    print(f"🔍 Setting title to '{job_title}'...")
                    title_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='desc' and @type='text']")))
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title_input)
                    time.sleep(1)
                    title_input.clear()
                    title_input.send_keys(job_title)
                    print(f" Title set to '{job_title}'")

                    print(" Clicking 'Submit'...")
                    max_retries = 3
                    retries = max_retries
                    while retries > 0:
                        try:
                            submit_btn = wait.until(EC.element_to_be_clickable((By.ID, "submit_workflow")))
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", submit_btn)
                            time.sleep(1)
                            submit_btn.click()
                            print(" 'Submit' clicked")
                            time.sleep(30)
                            return True
                        except WebDriverException as e:
                            retries -= 1
                            print(f"   Failed to click 'Submit' (Retry {max_retries - retries}/{max_retries}): {e}")
                            if retries == 0:
                                print("   Attempting JavaScript submit...")
                                try:
                                    driver.execute_script("ProteoSAFeInputUtils.submitInputForm();")
                                    print(" Fallback: Form submitted via JavaScript")
                                    time.sleep(30)
                                    return True
                                except WebDriverException as js_e:
                                    print(f"   JavaScript fallback failed: {js_e}")
                                    return False
                            time.sleep(5)
                else:
                    print(" Failed to configure advanced options")
            else:
                print(f" No .tsv file named {tsv_filename} selected")
        else:
            print(" No files selected")
        return False
    except Exception as e:
        print(f" ERROR: {e}")
        traceback.print_exc()
        return False
    finally:
        print(" Script finished")
        driver.quit()

if __name__ == "__main__":
    run_gnps_workflow("jibanp", "1234567890", "Bacillus_specific_metadata.tsv", "Aspergillus")