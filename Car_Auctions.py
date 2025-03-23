from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import pandas as pd
import re
from datetime import datetime
import pytz  # For handling time zones like AEDT
import time
from freezegun import freeze_time


def login_to_pickles(driver, username, password):
    for tries in range(5):
        try:
            wait = WebDriverWait(driver, 10)  # Set up WebDriverWait with a 10-second timeout

            # Click the 'Log In' button to open the login modal
            login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Log In']")))
            login_button.click()

            # Wait for the username input field to be present in the modal
            username_input = wait.until(EC.presence_of_element_located((By.ID, 'pickles-sign-in-username')))
            username_input.clear()
            username_input.send_keys(username)

            # Wait for the password input field to be present
            password_input = wait.until(EC.presence_of_element_located((By.ID, 'pickles-sign-in-password')))
            password_input.clear()
            password_input.send_keys(password)

            # Wait for the 'Log In' button to be clickable and then click it
            login_submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log In']")))
            login_submit_button.click()
            break
        except TimeoutException:
            print(f"Timeout waiting for login modal. Retrying {tries+1} of 5")
            continue

def open_future_events_section(driver):
    try:
        future_events_element = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='vc-more-dates futureDate-toggle']"))
        )
        future_events_element.click()
        print("Auction section opened.")
        return True
    except:
        print("Timeout: Could not open auction section.")
        return False

def navigate_back_until_target(driver, target_url_base):
    while True:
        current_url = driver.current_url

        # Check if the current URL starts with the target base URL, excluding the page number part
        if current_url.startswith(target_url_base):
            print(f"Reached target base URL: {current_url}")
            break  # Exit the loop if the URL matches the base target URL (excluding page number)
        else:
            print(f"Current URL: {current_url} does not match target, navigating back...")
            driver.back()  # Navigate back to the previous page
            time.sleep(2)  # Sleep for a short period to ensure the page has loaded


def create_driver(proxy=None, headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--window-size=1920,1080")  # Set window size for headless mode

    chrome_options.add_argument("--start-maximized")  # Open the browser in maximized mode
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")

    # Set proxy if provided
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_auction_links(driver):
    while True:
        # Wait for the cards to load
        time.sleep(3)

        try:
            # Find all cards that contain the "Bid Live" button
            bid_live_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@aria-label="Bid Live"]/button')))
        except:
            print("Failed to find 'Bid Live' buttons. Closing the Browser window")
            break
        # checking the verification of the account
        check_verification(driver)

        # Loop through those cards and collect the auction links
        for i in range(1 , len(bid_live_buttons) + 1):
            try:
                bid_live_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, f'(//div[@aria-label="Bid Live"]/button)[{i}]')))
                # Move to the element and click it
                ActionChains(driver).move_to_element(bid_live_button)
                time.sleep(1)  # Wait for the button to load before clicking it
                bid_live_button.click()  # Go to the auction page
                print("Clicked 'Bid Live' button.")

                # checking the verification of the account
                check_verification(driver , xpath='//button[@class="sale-registration_modalbutton__zg3Rr sale-registration_secondary__mnGSr sale-registration_justwatch__sio6k"]')

                # Wait for navigation to complete
                time.sleep(2)
                
                navigate_to_main_tab(driver)

                # Navigate back to the main page
                url = 'https://www.pickles.com.au/upcoming-auctions/cars-motorcycles'
                navigate_back_until_target(driver , url)
                try:
                    bid_live_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@aria-label="Bid Live"]/button')))
                    time.sleep(2)
                except:
                    print(f"Error waiting for bid live buttons: {e}")  # If the 'Bid Live' buttons are not found or clickable, break the loop

            except Exception as e:
                print(f"Error capturing auction link: {e}")
                continue

        # Find the pagination 'Next' button and check if it's enabled
        try:
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@id="np-next"]')))
            if "numbered-pagination_disabled__DE3tU" in next_button.get_attribute("class"):
                break  # No more pages, stop the loop
            next_button.click()  # Go to the next page
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking next button: {e}")
            break  # If the 'Next' button is not found or clickable, break the loop

def navigate_to_main_tab(driver):
    try:    
        main_window = driver.window_handles[0]

        # Close all other tabs in one go
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()

        # Switch back to the main window
        driver.switch_to.window(main_window)

    except Exception as e:
        print(f"Error in Registration: {e}")

def get_pickles_data(driver, username, password):
    for tries in range(5):
        try: 
            user_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@name='_58_login']")))
            user_input.send_keys('')
            user_input.send_keys(username)
            pass_input = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@name='_58_password']")))
            pass_input.send_keys('')
            pass_input.send_keys(password)
            login_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@id='sign-in-btn']")))
            login_button.click()
            print('Logged in to Pickles')
            break
        except Exception as e:
            print(f"Failed to login, attempt {tries+1}: {e}")
            time.sleep(5)
            continue

def check_verification(driver, xpath = None):
    try:
        if xpath is None:
            btn = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH , '//button[@class="sale-registration_closebutton__ovPx_"]'))) 
            btn.click()
        else:
            btn = WebDriverWait(driver , 10).until(EC.presence_of_element_located((By.XPATH , xpath)))
            btn.click()
    except Exception:
        print("Sale registration modal not found, continuing...")
        pass

# functions for extracting the data from the registered auctions
def open_future_events_section(driver):
    try:
        future_events_element = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='vc-more-dates futureDate-toggle']"))
        )
        future_events_element.click()
        print("Auction section opened.")
        return True
    except:
        print("Timeout: Could not open auction section.")
        return False

# Define function to extract auction details
def extract_auction_details(driver):
    open_future_events_section(driver)
    # aedt = pytz.timezone('Australia/Sydney')
    timezone_map = {
    "AEDT": "Australia/Sydney",
    "ACDT": "Australia/Adelaide",
    "AED": "Australia/Sydney",   # Add alternative abbreviations here as needed

    # Add other relevant time zones if needed
}
    auction_data = []
    try:
        closed_auction_btns = WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="xxx-parent"]'))
        )
        for closed_btn in range(len(closed_auction_btns)):
            try:
                xpath = f'(//a[@class="xxx-parent"])[{closed_btn+1}]'
                WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, xpath))
                ).click()
                time.sleep(1)
                auction_time_element = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                auction_time = auction_time_element.text.strip().split('\n')[0]

                auction_details_element = WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, xpath+'/small'))
                )
                auction_details = auction_details_element.text

                match = re.search(r'(.+) at (\d{2}/\d{2}/\d{4} \d{1,2}:\d{2} [APM]{2}) ([A-Z]{2,4})', auction_details)
                auction_type = match.group(1).strip() if match else "Unknown"
                auction_date_time_str = match.group(2).strip() if match else "Unknown"
                auction_time_zone = match.group(3).strip() if match else "Unknown"

                # Parse date and time without timezone first
                auction_date_time = datetime.strptime(auction_date_time_str, '%d/%m/%Y %I:%M %p')
                
                if auction_time_zone in timezone_map:
                    auction_date_time = pytz.timezone(timezone_map[auction_time_zone]).localize(auction_date_time)
                    current_time = datetime.now(pytz.timezone(timezone_map[auction_time_zone]))
                    print('current_time: ',current_time)
                    print('auction_date_time: ',auction_date_time)
                    # Check if the auction date is in the past or now
                    if auction_date_time <= current_time:
                        # car_data = extract_car_data(driver)
                        # print("Car data")
                        # for car in car_data:
                        #     auction_data.append({
                        #         "Auction Time": auction_time,
                        #         "Auction Type": auction_type,
                        #         "Auction Date and Time": auction_date_time_str,
                        #         "Car Details": car['Car Details'],
                        #         "Car Status": car['car_status'],
                        #         "Car Price": car['car_price'],
                        #         'stock_No': car['stock_No'],
                        #         "Car Specifications": car['Car Specifications'],
                        #         "Car Condition Report": car['Car Condition Report'],
                        #         "Image URLs": car['Image URLs'],
                        #     })

                        print(f"Auction data collected for auction on {auction_date_time_str}.")
                    else:
                        print(f"Skipped auction on {auction_date_time_str} as it's in the future.")
                else:
                    print(f"Unknown timezone {auction_time_zone} in auction details.")

                # Close the auction details popup
                WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.XPATH, f'//span[@class="view-lane XXX-lane-col on"]'))
                ).click()
                
            except Exception as e:
                print(f"Error extracting auction details: {e}")


    except Exception as e:
        print(f"Error opening closed auction buttons: {e}")

    return auction_data

# Define function to extract car data
def extract_car_data(driver):
    print("Extracting car data...")
    car_data = []
    try:
        car_data_rows = WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.XPATH, '//tbody[@class="vc-tbdy-vehlist"]/tr'))
        )
        
        for car_row in car_data_rows:
            car_link = car_row.find_element(By.XPATH, "./td/a[@class='vc-details']")

            try:    
                car_status = car_row.find_element(By.XPATH, "./td[@class='badge-row']").text
                car_price = car_row.find_element(By.XPATH, "./td[@class='price-row']").text
                
            except:
                print("Error getting car ssh status")
                car_price = "No price available"
                car_status = "No status available"
            car_link.click()
            time.sleep(5)

            try:
                h4_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='vc-pop-inner']//h4"))
                )
                car_details = h4_element.text

                print("Car Details , " + car_details)
                try:
                    specifications, stock_No = extract_car_specifications(driver)
                    condition_report, image_urls = extract_condition_report_and_images(driver)
                except Exception as e:
                    print(f"Error extracting car specifications and images: {e}")    
                car_data.append({
                    "Car Details": car_details,
                    'car_status': car_status,
                    'car_price': car_price,
                    'stock_No':stock_No,
                    "Car Specifications": specifications,
                    "Car Condition Report": condition_report,
                    "Image URLs": image_urls,
                })



                # Close the car details popup
                WebDriverWait(driver, 40).until(
                    EC.presence_of_element_located((By.XPATH, '//a[@class="vc-pop-close btn-close pull-right"]'))
                ).click()
                
            except Exception as e:
                print(f"Error extracting car details: {e}")

    except Exception as e:
        print(f"Error extracting car data rows: {e}")

    return car_data

# Define function to extract car specifications
def extract_car_specifications(driver):
    specifications = ''
    stock_NOs = []
    try:
        stock_no = WebDriverWait(driver, 40).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='margin-right10 item-stock-number']")))
        stock_no = stock_no.text.strip() if stock_no else "Unknown"
        stock_NOs.append(stock_no)
        data_rows = WebDriverWait(driver, 40).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//table[@class='table table-condensed table-striped f12']/tbody/tr"))
        )
        for row in data_rows:
            label = row.find_element(By.XPATH, "./td[1]").text.strip()
            value = row.find_element(By.XPATH, "./td[2]").text.strip()
            specifications += f"label: {label}, value: {value}\n"
    except Exception as e:
        print(f"Error extracting car specifications: {e}")
    return specifications, stock_no

# Define function to extract condition report and images
def extract_condition_report_and_images(driver):
    # condition_report = {}
    
    condition_report = ''
    try:
        condition_report_element = WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//a[@data-toggle="damage"]/div/span'))
        )
        condition_report_element.click()
        time.sleep(1)
        
        # Extract condition details for each part
        condition_table_rows = WebDriverWait(driver, 40).until(
            EC.presence_of_all_elements_located((By.XPATH, "//table[@class='table table-condensed table-striped f12']/tbody/tr"))
        )
        for con_row in condition_table_rows:
            part = con_row.find_element(By.XPATH, "./td[1]").text.strip()
            condition = con_row.find_element(By.XPATH, "./td[2]").text.strip()
            condition_report += f'Part: {part}: Condition: {condition}\n'
        # Extract image URLs
        images_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-toggle='images']/div/span"))
        )
        images_link.click()
        time.sleep(5)

        image_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='simplebar-content']//img[@class='image img-responsive']"))
        )
        image_urls = [img.get_attribute("src") for img in image_elements]
        time.sleep(2)
        
    except Exception as e:
        print(f"Error extracting condition report and images: {e}")

    return condition_report , image_urls
 

def registerAuctions(driver, link):
    print("Getting the Driver...")
    driver.get(link)
    print("Logging in")
    login_to_pickles(driver=driver, username='vishaal.dutt@gmail.com', password='Pickleshasabluelogo2023')
    time.sleep(1)
    check_verification(driver)
    get_auction_links(driver)
    print("Registeration completed................................................................")


def get_auction_data(driver, link):
    auction_data = []
    try:
        # link = 'https://us.pickles-au.velocicast.io/'
        driver.get(link)
        
        # login_to_pickles(driver, username, password)

        driver.implicitly_wait(2)
        check_verification(driver)
        try:
            redirect_btn = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Bid Live"]//button')))
            redirect_btn.click()
        except:
            print("Redirect button not found. Continuing with the script.")

        # driver.switch_to.window(driver.window_handles[-1])
        driver.implicitly_wait(2)
        auction_data = extract_auction_details(driver)
        
        # Save auction data to CSV
        df = pd.DataFrame(auction_data)
        if os.path.exists('./DataFile.csv') :
            os.remove('./DataFile.csv')
        df.to_csv("DataFile.csv", index=False)
        print("Data saved to auction_data.csv")
        
    except Exception as e:
        print(f"Error in main function: {e}")
        
    finally:
        driver.quit()



if __name__ == '__main__':
    driver = create_driver(headless=False)
    link = 'https://www.pickles.com.au/upcoming-auctions/cars-motorcycles/'
    registerAuctions(driver , link)
    # with freeze_time("2025-03-24 04:00 AM AEDT"):
    get_auction_data(driver, link)
    print("Close the driver")
    driver.quit()