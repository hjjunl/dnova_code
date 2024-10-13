import sys
import pandas as pd
import time
import pickle
import os
import re
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import random
from selenium.webdriver.common.action_chains import ActionChains

# Define the range for the random sleep time in seconds
min_sleep_time, max_sleep_time = 1, 3

# Function to create ChromeOptions and a new Chrome driver
def create_driver():
    """Create a new instance of Chrome driver with fresh ChromeOptions."""
    options = uc.ChromeOptions()
    options.headless = False
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en'})
    
    driver = uc.Chrome(options=options, use_subprocess=True)
    driver.set_window_size(1000, 800)
    return driver

initial_path = "C:/Users/HyunJunLee/Documents/hj_git/YouTube_Report_Automation/YouTube_Shorts_Automation/youtube_shorts_crawling/change_fixced url copy/change_fixced url copy/"
# List of cookie files to rotate through
cookie_files = [
    "cookies_list/cookies_hyunjun960214.pkl",
    "cookies_list/cookies_ytcollect1.pkl",
    "cookies_list/cookies_yttrendreport.pkl",
    # "cookies_list/cookies_data_nova.pkl"
]
cookie_index = 0

def login(driver):
    """Login to YouTube using the provided driver and rotating cookie files."""
    global cookie_index
    cookies_file_path = initial_path + cookie_files[cookie_index]
    print(f"Using cookies from: {cookies_file_path}")

    if os.path.exists(cookies_file_path):
        with open(cookies_file_path, 'rb') as cookies_file:
            cookies = pickle.load(cookies_file)
            driver.get('https://www.youtube.com')
            driver.implicitly_wait(10)
            for cookie in cookies:
                driver.add_cookie(cookie)
            print("Cookies added")
            driver.refresh()
            driver.implicitly_wait(10)
    else:
        driver.get('https://www.youtube.com')
        driver.implicitly_wait(15)
        try:
            clk = driver.find_element(By.XPATH, "(//div[@class='yt-spec-touch-feedback-shape yt-spec-touch-feedback-shape--touch-response-inverse'])[2]").click()
            time.sleep(random.uniform(1, 3))
        except:
            pass
        try:
            driver.find_element(By.XPATH, "//*[@id='buttons']/ytd-button-renderer/yt-button-shape/a/yt-touch-feedback-shape/div").click()
            time.sleep(random.uniform(1, 3))
            email_field = driver.find_element(By.XPATH, "//*[@id='identifierId']")
            email_field.send_keys("yttrendreport")
            time.sleep(random.uniform(1, 3))
            email_field.send_keys(Keys.ENTER)
            time.sleep(random.uniform(1, 3))
            email_pass = driver.find_element(By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")
            email_pass.send_keys("hjl960214!!")
            time.sleep(1)
            email_pass.send_keys(Keys.ENTER)
            time.sleep(random.uniform(1, 3))
            driver.implicitly_wait(10)
        except:
            pass
        with open(cookies_file_path, 'wb') as cookies_file:
            pickle.dump(driver.get_cookies(), cookies_file)
        print("Cookies saved")

    # Rotate to the next cookie file for the next login
    cookie_index = (cookie_index + 1) % len(cookie_files)

def get_latest_revised_number(revised_folder):
    """Get the largest number from the revised_url숫자.xlsx files in the revised_folder."""
    revised_files = [f for f in os.listdir(revised_folder) if re.match(r'revised_url(\d+)\.xlsx', f)]
    if not revised_files:
        return 0  # No files exist, so start from 0

    # Extract the numbers from filenames and find the largest one
    numbers = [int(re.search(r'revised_url(\d+)\.xlsx', f).group(1)) for f in revised_files]
    return max(numbers)

def get_starting_row(revised_file_path, split_file_path):
    """
    Get the row to start from by comparing the last row in the revised file 
    with the corresponding row in the split file.
    """
    if os.path.exists(revised_file_path):
        df_revised = pd.read_excel(revised_file_path)
        df_split = pd.read_excel(split_file_path)

        # Get the last URL from the revised file
        if not df_revised.empty:
            last_processed_url = df_revised['yt_url'].iloc[-1]  # 마지막 처리된 yt_url 가져오기
        else:
            return 0  # revised file is empty, start from the beginning

        # Find the index of the last processed URL in the split file
        for idx, row in df_split.iterrows():
            if row['yt_url'] == last_processed_url:
                print(f"Resuming from row {idx + 1} (next after last processed row) in split file.")
                return idx + 1  # Start from the next row after the last processed URL

        return len(df_split)  # If the URL is not found, start from the end
    return 0  # If no revised file, start from the first row

# Function to process each excel file
def process_excel_file(file_number, driver, revised_folder):
    """Process the Excel file and save the progress whenever an error occurs or the program ends."""
    df = pd.DataFrame(columns=['yt_title', 'yt_url', 'proceeded'])  # Initialize the DataFrame outside the try block
    try:
        # Get unprocessed rows
        split_file = f"{initial_path}split_data/split_{file_number}.xlsx"
        revised_file = f"{revised_folder}/revised_url{file_number}.xlsx"

        # Get the starting row
        start_row = get_starting_row(revised_file, split_file)

        # Read the split file
        df_split = pd.read_excel(split_file)

        if start_row >= len(df_split):
            print(f"All URLs in split_{file_number}.xlsx have been processed.")
            return

        for index, row in df_split.iterrows():
            if index < start_row:
                continue  # Skip rows that are already processed

            print(f"Processing split_{file_number}, row {index}")  # 현재 처리중인 파일과 행 번호 출력
            time.sleep(random.uniform(1, 2))
            try:
                url = row['yt_url']
                title = row['channel_name']
                driver.get(url.strip())
                driver.implicitly_wait(10)
                fixed_url = driver.current_url
                print("fixed_url: ", fixed_url)
                new_data = [title, fixed_url + "/short", "proceeded"]
                df.loc[len(df)] = new_data
            except Exception as err:
                print(f"Error processing {title} at row {index} in split_{file_number}.xlsx: {err}")
                # Save the current progress when an error occurs
                output_file = f"{revised_folder}/revised_url{file_number}.xlsx"
                df.to_excel(output_file, index=False)
                print(f"Progress saved up to row {index} in file: {output_file}")
                raise  # Re-raise the exception to be caught by the main loop

    except Exception as e:
        print(f"Error processing file {file_number}: {e}")
        raise  # Re-raise the exception to be caught by the main loop

    finally:
        # Always save progress whether there's an error or the program is manually stopped
        output_file = f"{revised_folder}/revised_url{file_number}.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Progress saved for file {file_number}: {output_file}")

# Main execution function
def execute_crawling():
    revised_folder = initial_path + "revised_folder"
    
    # Find the latest revised file number
    latest_revised_number = get_latest_revised_number(revised_folder)
    print(f"Starting from the latest revised file: revised_url{latest_revised_number}.xlsx")
    
    # Start from split_300.xlsx onwards
    for i in range(213, 299):
        driver = None
        try:
            # Create a new driver instance for each file
            driver = create_driver()
            login(driver=driver)

            # Process the current file
            process_excel_file(i, driver, revised_folder)
            print(f"Processed file {i}. Waiting before the next file...")
            time.sleep(random.uniform(30, 60))  # Sleep for 30-60 seconds between each run
        except Exception as e:
            print(f"Error occurred while processing file {i}: {e}. Restarting with a new cookie.")
            
            # Ensure the driver is closed after an error
            if driver:
                driver.quit()
            
            # Sleep and retry with a new cookie
            time.sleep(random.uniform(120, 150))  # Wait for 2-2.5 minutes before retrying

            # Use a new cookie and retry processing the same file
            driver = create_driver()  # Recreate the driver with fresh ChromeOptions
            login(driver=driver)
            try:
                process_excel_file(i, driver, revised_folder)
            except Exception as retry_error:
                print(f"Failed again while processing file {i}: {retry_error}. Skipping to next file.")
                continue  # Skip to the next file if it fails again

        finally:
            # Ensure the driver is closed after processing each file, or in case of an error
            if driver:
                driver.quit()

# Execute the crawling process
execute_crawling()
