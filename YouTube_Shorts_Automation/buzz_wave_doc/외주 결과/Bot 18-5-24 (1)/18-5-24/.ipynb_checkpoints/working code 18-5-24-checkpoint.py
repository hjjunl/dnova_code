
import pandas as pd
from datetime import datetime, timedelta
import csv
import time
import pickle
from selenium.webdriver.common.by import By
import os
from openpyxl import Workbook
from openpyxl import load_workbook
import undetected_chromedriver as uc
import os
import csv
import tkinter as tk
from tkinter import simpledialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
# Import the necessary module
from bs4 import BeautifulSoup
import random

# Define the range for the random sleep time in seconds
min_sleep_time, max_sleep_time = 1, 3

# Generate and use a random sleep time within the defined range
random_sleep=time.sleep(random.uniform(min_sleep_time, max_sleep_time))



options = uc.ChromeOptions()
options.headless = False

driver = uc.Chrome(options=options, use_subprocess=True)
# Set the browser window size
driver.set_window_size(1000, 800)
####################################################################

def check_folder_empty(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return not any(filename.endswith('.csv') for filename in os.listdir(folder))

def split_csv(input_file, output_folder, max_records=500):
    if not check_folder_empty(output_folder):
        print("CSV files already exist in the output folder. Skipping splitting.")
        return

    with open(input_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Read the header

        count = 0
        file_index = 1
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, f'split_{file_index}.csv')
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)  # Write the header to each split file
            for row in reader:
                writer.writerow(row)
                count += 1
                if count == max_records:
                    count = 0
                    file_index += 1
                    output_file = os.path.join(output_folder, f'split_{file_index}.csv')
                    outfile.close()  # Close the current file
                    outfile = open(output_file, 'w', newline='')  # Reopen the file
                    writer = csv.writer(outfile)
                    writer.writerow(header)


def crawler(output_folder, csv_file_index):
    csv_files = [filename for filename in os.listdir(output_folder) if filename.endswith('.csv')]
    if not csv_files:
        print("No CSV files found in the split folder.")
        return None
    else:
        if csv_file_index < 1 or csv_file_index > len(csv_files):
            print("Invalid CSV file index.")
            return None
        else:
            return os.path.join(output_folder, csv_files[csv_file_index - 1])

# Example usage:
input_file = 'links.csv'  # Replace 'input.csv' with your CSV file path
output_folder = 'split-csv'  # Folder where split CSV files will be saved
split_csv(input_file, output_folder, max_records=500)

# Select a CSV file from the split folder
csv_link_file =  crawler(output_folder, csv_file_index=1)
print("Selected CSV file:", csv_link_file)





##################################################

import re


def convert_subscriber_count(subscriber_str):
    match = re.match(r"(\d+(\.\d+)?)([MK]?)", subscriber_str, re.IGNORECASE)
    if match:
        number = float(match.group(1))
        suffix = match.group(3).upper()

        if suffix == 'M':
            return int(number * 1_000_000)
        elif suffix == 'K':
            return int(number * 1_000)
        else:
            return int(number)  # No suffix, return the number as is
    return int(subscriber_str)  # If input format is unexpected, try returning it as integer



#############

def login(driver, cookies_file_path='cookies.pkl'):
    if os.path.exists(cookies_file_path):
        # Load cookies if the file exists
        with open(cookies_file_path, 'rb') as cookies_file:
            cookies = pickle.load(cookies_file)
            # Use the loaded cookies for the session
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
            clk=driver.find_element(By.XPATH,"(//div[@class='yt-spec-touch-feedback-shape yt-spec-touch-feedback-shape--touch-response-inverse'])[2]").click()
            time.sleep(random.uniform(1, 3))
            driver.implicitly_wait(10)
        except:
            pass
        try:
            driver.find_element(By.XPATH,"//*[@id='buttons']/ytd-button-renderer/yt-button-shape/a/yt-touch-feedback-shape/div").click()
            time.sleep(random.uniform(1, 3))
            driver.implicitly_wait(10)
            element=driver.find_element(By.XPATH,"//*[@id='identifierId']").click()
            print("cLICKED")
            # Find and input the email/username
            email_field = driver.find_element(By.XPATH, "//*[@id='identifierId']")
            email_field.send_keys("darkjhon449")  # Replace with your email/username
            time.sleep(random.uniform(1, 3))  # Adding a delay to ensure the text is inputted before continuing

            # Press Enter to proceed to the password input
            email_field.send_keys(Keys.ENTER)
            time.sleep(random.uniform(1, 3))  # Adding a delay to ensure the page loads properly
            driver.implicitly_wait(10)

            email_pass = driver.find_element(By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")
            email_pass.send_keys("Pakistan@1947")  # Replace with your email/username
            time.sleep(1)  # Adding a delay to ensure the text is inputted before continuing

            # Press Enter to proceed to the password input
            email_pass.send_keys(Keys.ENTER)
            time.sleep(random.uniform(1, 3)) # Adding a delay to ensure the page loads properly
            driver.implicitly_wait(10)
            input()



        except:
            pass





        # Save cookies for future use
        with open(cookies_file_path, 'wb') as cookies_file:
            pickle.dump(driver.get_cookies(), cookies_file)
        print("cookies saved")

login(driver=driver)




def create_csv_files():
    # Create a folder named "successful_Data" if it doesn't exist
    headers = ["chanel_name", "yt_url", "subscribers", "check_date", "released_date", "is_posted_in_date_range",
               "shorts_name", "description", "likes", "views", "short_url"]
    headers2 = ["yt_url", "check_date", "is_posted_in_date_range"]

    folder_name = "successful_Data"
    folder_name2 = "failed_Data"

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created successfully.")

    if not os.path.exists(folder_name2):
        os.makedirs(folder_name2)
        print(f"Folder '{folder_name2}' created successfully.")

    # Get the current date in the desired format
    current_date = datetime.now().strftime("-%d-%m-%Y")
    file_name = os.path.join(folder_name, f"data{current_date}.csv")

    # Check if a file with the current date exists
    if not os.path.exists(file_name):
        # If it doesn't exist, create a new CSV file with that name

        pd.DataFrame(columns=headers).to_csv(file_name, index=False)
        print(f"CSV file '{file_name}' created successfully.")
    else:
        print(f"CSV file '{file_name}' already exists.")

    # Create CSV files in "failed_Data" folder
    failed_folder_name = "failed_Data"
    Banned_or_no_short_video = os.path.join(failed_folder_name, "No_Short_Videos_Or_Banned.csv")
    no_video_in_date_range = os.path.join(failed_folder_name, f"No_Short_Video_in_date-Range{current_date}.csv")

    # Check if the files already exist
    if not os.path.exists(Banned_or_no_short_video):
        # Create the file only if it doesn't exist
        pd.DataFrame(columns=headers2).to_csv(Banned_or_no_short_video, index=False)
        print(f"CSV file '{Banned_or_no_short_video}' created successfully.")
    else:
        print(f"CSV file '{Banned_or_no_short_video}' already exists.")

    if not os.path.exists(no_video_in_date_range):
        # Create the file only if it doesn't exist
        pd.DataFrame(columns=headers).to_csv(no_video_in_date_range, index=False)
        print(f"CSV file '{no_video_in_date_range}' created successfully.")
    else:
        print(f"CSV file '{no_video_in_date_range}' already exists.")

    return file_name, Banned_or_no_short_video, no_video_in_date_range

csv_file, Banned_or_no_short_video1, no_video_in_date_range1 = create_csv_files()



###################################
headers = ["chanel_name", "yt_url", "subscribers", "check_date", "released_date", "is_posted_in_date_range",
           "shorts_name", "description", "likes", "views", "short_url"]

df = pd.DataFrame(columns=headers)
check_date = datetime.now().strftime("%d-%m-%Y")
print(check_date)
############################################

while True:
    try:

        # Read channel URLs from the CSV file
        with open(csv_link_file, "r") as file:
            reader = csv.DictReader(file)
            rows = list(reader)  # Convert the reader object to a list of rows for easier access
            for index, row in enumerate(rows):
                check_date = datetime.now().strftime("%d-%m-%Y")
                url = row['links']
                processed = row['processed']
                if not processed:  # Process only if 'processed' column is empty
                    # print(url)
                    chanel_url = url  # Store the URL in chanel_url variable
                    print(f"Processing link  ##  " + url)

                    print("loading url")
                    # Load the channel URL in the browser
                    driver.get(url.strip())  # Strip any leading/trailing whitespaces
                    driver.implicitly_wait(10)
                    fixed_url = driver.current_url

                    # Update the processed column for the current URL to 'Yes'
                    rows[index]['processed'] = 'Yes'

                    # Write back to the CSV file with updated data
                    with open(csv_link_file, "w", newline='') as csvfile:
                        fieldnames = ['links', 'processed']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(rows)
                     # Break the loop after processing the current URL

                    time.sleep(2)

                    # Get page source
                    page_source = driver.page_source

                    # Parse page source using BeautifulSoup
                    soup = BeautifulSoup(page_source, 'html.parser')

                    # Extract all text from the page
                    all_text = soup.get_text()
                    # print(all_text)

                    # Using regular expression to extract subscribers count
                    subscribers_pattern = re.search(r'(\d+(?:\.\d+)?[KM]?)(?=\s*subscribers)', all_text, re.IGNORECASE)
                    if subscribers_pattern:
                        subscribers = subscribers_pattern.group().strip()
                        #############################


                        subscriber_str =subscribers


                        subscribers = convert_subscriber_count(subscriber_str)

                        print("Subscribers:", subscribers)


                    else:
                        subscribers=""
                        print("Subscribers not found.")

                    # Using regular expression to extract channel name
                    channel_pattern = re.search(r'(.+)(?= - YouTube)', all_text)
                    if channel_pattern:
                        channel_name = channel_pattern.group().strip()
                        print("Channel Name:", channel_name)
                    else:
                        channel_name=""
                        print("Channel name not found.")


                    if (
                            " terminated because we received multiple third-party claims of copyright" in all_text or "This channel is not available" in all_text or "This channel does not exist" in all_text or "The page you were looking for doesn't exist" in all_text or
                            "account has been terminated because it is linked to an account that received multiple third-party claims of copyright infringement" in all_text) or "channel was removed because it violated our Community Guidelines" in all_text:

                        print("banned account")
                        #saving data
                        new_row = {'yt_url': fixed_url,
                                   'check_date': check_date,
                                   'is_posted_in_date_range': "Banned"}

                        ##################################################################################################################################
                        print("Trying 1")
                        ############################################
                        fieldnames = ['yt_url', 'check_date', 'is_posted_in_date_range']

                        # Check if the file is empty
                        with open(Banned_or_no_short_video1, 'a', encoding='utf-8', newline='') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerow(new_row)  # Append the new row



                        print("New row appended successfully.")

                        print("data is saved")
                        break
                    ##############################################
                    # Get the page source
                    page_source = driver.page_source

                    # Parse the page source using BeautifulSoup
                    soup = BeautifulSoup(page_source, 'html.parser')

                    # Find the element matching the XPath
                    element = soup.find("yt-tab-shape", {"tab-title": "Shorts"})

                    #######################################
                    find_short = None
                    short_xpath = "//*[@id='tabsContent']/yt-tab-group-shape/div[1]/yt-tab-shape[{}]"

                    for i in range(1, 4):  # Try different indexes from 1 to 9
                        try:
                            short_xpath_formatted = short_xpath.format(i)
                            find_short = driver.find_element(By.XPATH, short_xpath_formatted).text
                            if "Shorts" in find_short:
                                print(f"Found 'Shorts' at XPath: {short_xpath_formatted}")
                                click_short = driver.find_element(By.XPATH, short_xpath_formatted).click()
                                break
                        except:
                            pass

                    if find_short is None:
                        print("Text 'Shorts' not found in any of the XPaths.")
                        # saving data
                        new_row = {'yt_url': fixed_url,
                                   'check_date': check_date,
                                   'is_posted_in_date_range': "No short Videos"}

                        ##################################################################################################################################
                        print("Trying 2")
                        ############################################
                        # Define the header and new row
                        fieldnames = ['yt_url', 'check_date',
                                      'is_posted_in_date_range']

                        # Check if the file is empty

                        with open(Banned_or_no_short_video1, 'a', encoding='utf-8', newline='') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerow(new_row)  # Append the new row

                        print("New row appended successfully.")

                        print("data is saved")

                        continue

                    else:
                        print(find_short)


                    shorts = driver.find_elements(By.XPATH,
                                                  "//a[@class='yt-simple-endpoint focus-on-expand style-scope ytd-rich-grid-slim-media']")
                    print(len(shorts))

                    if shorts is None or len(shorts) < 1:

                        print("No Short Videos loop breaked")
                        # saving data
                        new_row = {'yt_url': fixed_url,
                                   'check_date': check_date,
                                   'is_posted_in_date_range': "No short Videos"}

                        ##################################################################################################################################
                        print("Trying 3")
                        ############################################
                        # Define the header and new row
                        fieldnames = ['yt_url', 'check_date',
                                      'is_posted_in_date_range']

                        # Check if the file is empty
                        with open(Banned_or_no_short_video1, 'a', encoding='utf-8', newline='') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writerow(new_row)  # Append the new row



                        print("New row appended successfully.")
                        print("data is saved")


                        print(
                            "33333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")
                        break

                    # Store links in a list
                    links = []




                    for short in shorts:
                        link = short.get_attribute("href")
                        links.append(link)
                        # print(link)




                    print("all links saved")
                    # Set a flag to keep track of whether the 'if' part of the loop has executed
                    if_part_executed = False
                    # Iterate over the links and load them one by one

                    for link in links:
                        print("Loading link:", link)
                        driver.get(link)
                        driver.implicitly_wait(10)
                        try:

                            short_name = driver.find_element(By.XPATH,
                                                             "//h2[@class='title style-scope reel-player-header-renderer']").text
                        except:
                            continue

                        print(short_name)

                        time.sleep(random.uniform(1, 3))

                       # print("click1")
                        clk = driver.find_element(By.XPATH,
                                                 "//*[@id='button-shape']/button/yt-touch-feedback-shape/div/div[2]").click()
                        #print("click2")
                        time.sleep(random.uniform(1, 3))
                        clk2 = driver.find_element(By.XPATH,"//*[@id='contentWrapper']/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer").click()
                                                 #  "//*[@id='items']/ytd-menu-service-item-renderer/tp-yt-paper-item/yt-formatted-string").click()
                        print("clicked 3")

                        description_text = driver.find_element(By.XPATH,
                                                               "//*[@id='watch-while-engagement-panel']/ytd-engagement-panel-section-list-renderer[2]").text

                        #print(description_text)


                        text = description_text.replace("Description", "")
                        text = text.strip()  # To remove any leading or trailing whitespace

                        # Split the text into lines
                        lines = text.strip().split('\n')

                        # Find the index of the line containing 'Views'
                        views_index = -1
                        for i, line in enumerate(lines):
                            if 'Views' in line:
                                views_index = i
                                break

                        # Remove the 'Views' line, the three lines above it, and the two lines below it
                        if views_index >= 3 and views_index + 2 < len(lines):
                            lines = lines[:views_index - 3] + lines[views_index + 2 + 1:]

                        # Join the remaining lines back into a single string
                        cleaned_text = '\n'.join(lines)

                        description = cleaned_text
                        print("description:::::  ", cleaned_text)

                        ###########################
                        # Split the text into lines
                        lines = text.strip().split('\n')

                        # Find the index of the line containing 'Likes'
                        likes_index = -1
                        for i, line in enumerate(lines):
                            if 'Likes' in line:
                                likes_index = i
                                break

                        # Save the line above 'Likes' as the likes variable
                        if likes_index > 0:
                            likes = lines[likes_index - 1]
                        else:
                            likes = None  # Handle the case where there is no line above 'Likes'

                        # Output the likes variable
                        print(f"Likes are : {likes}")

                        # Find the index of the line containing 'Views'
                        Views_index = -1
                        for i, line in enumerate(lines):
                            if 'Views' in line:
                                Views_index = i
                                break

                        # Save the line above 'Likes' as the likes variable
                        if Views_index > 0:
                            veiws = lines[Views_index - 1]
                        else:
                            veiws = None  # Handle the case where there is no line above 'Likes'

                        # Output the likes variable
                        print(f"Views are : {veiws}")

                        # Split the text into lines
                        lines = text.strip().split('\n')

                        # Find the index of the line containing 'Views'
                        views_index = -1
                        for i, line in enumerate(lines):
                            if 'Views' in line:
                                views_index = i
                                break

                        # Save the two lines below 'Views'
                        if views_index != -1 and views_index + 2 < len(lines):
                            below_views = lines[views_index + 1:views_index + 3]
                        else:
                            below_views = []  # Handle the case where there are fewer than two lines below 'Views'

                        # Join the lines below 'Views' into a single string
                        below_views_combined = ' '.join(below_views)
                        date_str = below_views_combined

                        # Output the combined lines
                        print(f"date is ::::  {below_views_combined}")

                        time.sleep(1)
                        print("+" * 100)



                        try:
                            # Try parsing the date assuming it's in the format "Apr 26 2024"
                            date_obj = datetime.strptime(date_str, "%b %d %Y")
                        except ValueError:
                            # If ValueError occurs, try parsing the date assuming it's in the format "26 Apr 2024"
                            date_obj = datetime.strptime(date_str, "%d %b %Y")
                            # try:
                            #
                            #
                            # except ValueError:
                            #     # If ValueError occurs again, try parsing the date assuming it's in the format "2022 Dec 19"
                            #     date_obj = datetime.datetime.strptime(date_str, "%Y %b %d")

                        # Format the date consistently
                        date = date_obj.strftime("%b %d %Y")
                        print("date   :::" , date)




                        # Get the current date
                        current_date = datetime.now()

                        # Generate a list of date strings for the past 7 days
                        date_range = [(current_date - timedelta(days=i)).strftime("%b %d %Y") for i in range(7)]
                        # Print the generated date range
                        # print("Date Range (Past 7 days):")

                        # for dates in date_range:
                        #     print(dates)


                        # Check if the date falls within the past 7 days
                        if (date in date_range) or ("ago" in date.lower()):

                            if_part_executed = True



                            new_row = {'chanel_name': channel_name, 'yt_url': fixed_url,
                                       'subscribers': subscribers,
                                       'check_date': check_date, 'released_date': date,
                                       'is_posted_in_date_range': "Yes", 'shorts_name': short_name,
                                       'description': description, 'likes': likes, 'views': veiws,
                                       'short_url': link}
                            print(new_row)
                            #time.sleep(5)

                            ##################################################################################################################################
                            print("Trying 4")
                            ############################################

                            # Define the header and new row
                            fieldnames = ['chanel_name', 'yt_url', 'subscribers', 'check_date', 'released_date',
                                          'is_posted_in_date_range', 'shorts_name', 'description', 'likes', 'views',
                                          'short_url']

                            with open(csv_file, 'a', encoding='utf-8', newline='') as csvfile:
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                writer.writerow(new_row)  # Append the new row



                            print("New row appended successfully.")

                            print("data is saved")

                            print("loop is continueing")


                            print("%" * 100)
                            print(
                                "4444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444444")

                        else:
                            if not if_part_executed:  # If the 'if' part hasn't executed in the first iteration

                                check_date = datetime.now().strftime("%d-%m-%Y")
                                new_row = {'chanel_name': channel_name, 'yt_url': fixed_url,
                                           'subscribers': subscribers,
                                           'check_date': check_date, 'released_date': date,
                                           'is_posted_in_date_range': "No",
                                           'shorts_name': short_name,
                                           'description': description,
                                           'likes': likes, 'views': veiws, 'short_url': link}
                                print(new_row)
                                #time.sleep(5)
                                print("Trying 5")
                                ############################################
                                # Define the header and new row
                                fieldnames = ['chanel_name', 'yt_url', 'subscribers', 'check_date', 'released_date',
                                              'is_posted_in_date_range', 'shorts_name', 'description', 'likes', 'views',
                                              'short_url']

                                with open(no_video_in_date_range1, 'a', encoding='utf-8', newline='') as csvfile:
                                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                    writer.writerow(new_row)  # Append the new row

                                print("New row appended successfully.")
                                print("data is saved")


                                print("loop breaked")

                                print(
                                    "555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")

                                break
                            if (date not in date_range) or ("ago"  not in date.lower()):
                                print("breaking loop after saving data")
                                time.sleep(3)

                                break




    except Exception as e:
        #print(e)
        #input()

        pass








