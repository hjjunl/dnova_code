import sys

import pandas as pd
from datetime import datetime, timedelta

import time
import pickle
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc
import os
import csv

from selenium.webdriver.common.keys import Keys
import re

from bs4 import BeautifulSoup
import random
from selenium.webdriver.common.action_chains import ActionChains

import pymysql
from sqlalchemy import create_engine, text


# Define the range for the random sleep time in seconds
min_sleep_time, max_sleep_time = 1, 3

# Generate and use a random sleep time within the defined range
random_sleep=time.sleep(random.uniform(min_sleep_time, max_sleep_time))


options = uc.ChromeOptions()
options.headless = False
options.add_argument('--lang=en')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US,en'})


driver = uc.Chrome(options=options, use_subprocess=True)
# Set the browser window size
driver.set_window_size(1000, 800)


actions = ActionChains(driver)

#################################################################################################################################################
# Select a CSV file with absolute path

# crawler_input_csv_file= "split-csv/split_1.csv"

crawler_input_csv_file= "C:/Users/HyunJunLee/Documents/hj_git/YouTube_Report_Automation/YouTube_Shorts_Automation/youtube_shorts_crawling/youtube_bot_0901/youtube_bot_0806/split-csv/split_1.csv"



csv_link_file = crawler_input_csv_file
print("Selected CSV file:", csv_link_file)
df2 = pd.read_csv(csv_link_file)
print(df2)

##################################################



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

def login(driver, cookies_file_path='cookies_hyunjun960214.pkl'):
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
            email_field.send_keys("hyunjun960214")  # Replace with your email/username
            time.sleep(random.uniform(1, 3))  # Adding a delay to ensure the text is inputted before continuing

            # Press Enter to proceed to the password input
            email_field.send_keys(Keys.ENTER)
            time.sleep(random.uniform(1, 3))  # Adding a delay to ensure the page loads properly
            driver.implicitly_wait(10)

            email_pass = driver.find_element(By.XPATH, "//*[@id='password']/div[1]/div/div[1]/input")
            email_pass.send_keys("hjl960214")  # Replace with your email/username
            time.sleep(1)  # Adding a delay to ensure the text is inputted before continuing

            # Press Enter to proceed to the password input
            email_pass.send_keys(Keys.ENTER)
            time.sleep(random.uniform(1, 3)) # Adding a delay to ensure the page loads properly
            driver.implicitly_wait(10)
            # input()



        except:
            pass





        # Save cookies for future use
        with open(cookies_file_path, 'wb') as cookies_file:
            pickle.dump(driver.get_cookies(), cookies_file)
        print("cookies saved")

login(driver=driver)

def create_csv_files(ind):
    # Create a folder named "successful_Data" if it doesn't exist
    headers = ["chanel_name", "yt_url", "subscribers", "check_date", "released_date", "is_posted_in_date_range",
               "shorts_name", "description", "likes", "views", "short_url", "thumbnail_link"]
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
    file_name = os.path.join(folder_name, f"data{current_date}_{ind}.csv")

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
    no_video_in_date_range = os.path.join(failed_folder_name, f"No_Short_Video_in_date-Range{current_date}_{ind}.csv")

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

# 바꿔야 하는 곳
csv_file, Banned_or_no_short_video1, no_video_in_date_range1 = create_csv_files(0)
# csv_file, Banned_or_no_short_video1, no_video_in_date_range1 = create_csv_files(1)
#csv_file, Banned_or_no_short_video1, no_video_in_date_range1 = create_csv_files(2)
#csv_file, Banned_or_no_short_video1, no_video_in_date_range1 = create_csv_files(3)

headers = ["chanel_name", "yt_url", "subscribers", "check_date", "released_date", "is_posted_in_date_range",
           "shorts_name", "description", "likes", "views", "short_url", "thumbnail_link"]

df = pd.DataFrame(columns=headers)
check_date = datetime.now().strftime("%d-%m-%Y")

print(check_date)




# Initialize DataFrames to store data
df_banned_or_no_short_video = pd.DataFrame(columns=["yt_url", "check_date", "is_posted_in_date_range"])
df_successful = pd.DataFrame(columns=headers)
df_no_video_in_date_range = pd.DataFrame(columns=headers)


print(check_date)



# Read the CSV file into a DataFrame
df2 = pd.read_csv(csv_link_file)
print(df2)
processed_all_urls = False
while True:

        # Iterate over each row in the DataFrame
        for index, row in df2.iterrows():
            try:
                url = row['links']
                processed = row['processed']
                if not pd.notna(processed):  # Process only if 'processed' column is empty or NaN
                    print(f"Processing link  ##  {url}")

                    print("loading url")
                    # Load the channel URL in the browser
                    driver.get(url.strip())  # Strip any leading/trailing whitespaces
                    driver.implicitly_wait(10)
                    fixed_url = driver.current_url

                    # Update the processed column for the current URL to 'Yes'
                    df2.at[index, 'processed'] = 'Yes'
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

                        subscriber_str = subscribers

                        subscribers = convert_subscriber_count(subscriber_str)

                        print("Subscribers:", subscribers)


                    else:
                        subscribers = ""
                        print("Subscribers not found.")

                    # Using regular expression to extract channel name
                    channel_pattern = re.search(r'(.+)(?= - YouTube)', all_text)
                    if channel_pattern:
                        channel_name = channel_pattern.group().strip()
                        print("Channel Name:", channel_name)
                    else:
                        channel_name = ""
                        print("Channel name not found.")

                    if (
                            " terminated because we received multiple third-party claims of copyright" in all_text or "This channel is not available" in all_text or "This channel does not exist" in all_text or "The page you were looking for doesn't exist" in all_text or
                            "account has been terminated because it is linked to an account that received multiple third-party claims of copyright infringement" in all_text) or "channel was removed because it violated our Community Guidelines" in all_text:
                        print("banned account")
                        # saving data
                        new_row = {'yt_url': fixed_url,
                                   'check_date': check_date,
                                   'is_posted_in_date_range': "Banned"}

                        ##################################################################################################################################
                        print("Trying 1")
                        ############################################

                        # Convert new_row to a DataFrame
                        new_row_df = pd.DataFrame([new_row])

                        # Concatenate the existing DataFrame with the new row
                        df_banned_or_no_short_video = pd.concat([df_banned_or_no_short_video, new_row_df], ignore_index=True)



                        #df_banned_or_no_short_video.to_csv(Banned_or_no_short_video1, index=False)
                        print("New row appended successfully.")

                        print("data is saved")
                        continue
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

                        # Convert new_row to a DataFrame
                        new_row_df = pd.DataFrame([new_row])
                        # Concatenate the existing DataFrame with the new row
                        df_banned_or_no_short_video = pd.concat([df_banned_or_no_short_video, new_row_df],
                                                                ignore_index=True)

                        #df_banned_or_no_short_video.to_csv(Banned_or_no_short_video1, index=False)
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

                        # Convert new_row to a DataFrame
                        new_row_df = pd.DataFrame([new_row])
                        # Concatenate the existing DataFrame with the new row
                        df_banned_or_no_short_video = pd.concat([df_banned_or_no_short_video, new_row_df],
                                                                ignore_index=True)

                        #df_banned_or_no_short_video.to_csv(Banned_or_no_short_video1, index=False)
                        print("New row appended successfully.")
                        print("data is saved")

                        print(
                            "33333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")


                    thumbnail_tab = driver.find_element(By.XPATH,
                                                        "(//div[@class='style-scope ytd-two-column-browse-results-renderer'])[1]")
                    thumbnails = thumbnail_tab.find_elements(By.XPATH, ".//yt-image/img")
                    print(len(thumbnails))

                    links_with_thumbnails = []
                    i = 1
                    for thumbnail in thumbnails:
                        driver.execute_script("arguments[0].scrollIntoView();", thumbnail)
                        time.sleep(0.5)  # Adjust sleep time as needed

                        # Error handling (optional): Check if thumbnail has a valid 'src' attribute
                        if thumbnail.get_attribute("src"):
                            thumbnail_link = thumbnail.get_attribute("src")
                            # Extract the link from the 'short' element if possible
                            link = None
                            if short := thumbnail.find_element(By.XPATH, "./ancestor::*[@href]"):
                                link = short.get_attribute("href")

                            # Combine link and thumbnail into a tuple (assuming link is found)
                            if link:
                                links_with_thumbnails.append((link, thumbnail_link))

                        i = 1 + i
                        if i >= 11:
                            print("breaked")
                            break

                    print(links_with_thumbnails)

                    print("All links and thumbnails saved")

                    # Set a flag to keep track of whether the 'if' part of the loop has executed
                    if_part_executed = False
                    # Iterate over the links and load them one by one

                    # Iterate over the links and load them one by one
                    for link, thumbnail_link in links_with_thumbnails:
                        print("Loading link:", link)
                        print("Thumbnail link:", thumbnail_link)
                        if "watch" in link:
                            continue
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
                        # print("click2")
                        time.sleep(random.uniform(1, 3))
                        clk2 = driver.find_element(By.XPATH,
                                                   "//*[@id='contentWrapper']/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer").click()
                        #  "//*[@id='items']/ytd-menu-service-item-renderer/tp-yt-paper-item/yt-formatted-string").click()
                        print("clicked 3")

                        description_text = driver.find_element(By.XPATH,
                                                               "//*[@id='watch-while-engagement-panel']/ytd-engagement-panel-section-list-renderer[2]").text

                        # print(description_text)

                        text = description_text.replace("Description", "")
                        text = text.strip()  # To remove any leading or trailing whitespace

                        # Split the text into lines
                        lines = text.strip().split('\n')
                        print(f"lines::: {lines}")

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
                        if "Ago" in date_str:
                            # Get the current date and time
                            now = datetime.now()

                            # Format the date as "Jun 14 2024"
                            formatted_date = now.strftime("%b %d %Y")

                            # Print the formatted date
                            #print(formatted_date)

                            date_str = formatted_date

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
                        print("date   :::", date)

                        # Get the current date
                        current_date = datetime.now()

                        # Generate a list of date strings for the past 7 days
                        date_range = [(current_date - timedelta(days=7)).strftime("%b %d %Y"), current_date.strftime("%b %d %Y")]
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
                                       'short_url': link,
                                       'thumbnail_link': thumbnail_link}
                            print(new_row)
                            # time.sleep(5)

                            ###############################################################################################################################################################################################
                            print("Trying 4")
                            ############################################
                            # Convert new_row to a DataFrame
                            new_row_df = pd.DataFrame([new_row])



                            # Concatenate the existing DataFrame with the new row
                            df_successful = pd.concat([df_successful, new_row_df],
                                                                  ignore_index=True)

                            #df_successful.to_csv(csv_file, index=False)


                            print("New row appended successfully.")



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
                                           'likes': likes, 'views': veiws, 'short_url': link,
                                           'thumbnail_link': thumbnail_link}
                                print(new_row)
                                # time.sleep(5)
                                print("Trying 5")
                                ############################################
                                # Convert new_row to a DataFrame
                                new_row_df = pd.DataFrame([new_row])


                                # Concatenate the existing DataFrame with the new row
                                df_no_video_in_date_range = pd.concat([df_no_video_in_date_range, new_row_df],
                                                                        ignore_index=True)

                                #df_no_video_in_date_range.to_csv(no_video_in_date_range1, index=False)




                                print("loop breaked")

                                print(
                                    "555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")

                                break
                            if (date not in date_range) or ("ago" not in date.lower()):
                                print("breaking loop after saving data")
                                time.sleep(3)

                                break
            except Exception as e:
                #print(f"An error occurred: {e}")
                pass

        # saving dataframe data to csv files
        df2.to_csv(csv_link_file, index=False)
        df_banned_or_no_short_video.to_csv(Banned_or_no_short_video1, index=False)
        df_successful.to_csv(csv_file, index=False)
        df_no_video_in_date_range.to_csv(no_video_in_date_range1, index=False)

        print("input file updated ")

        processed_all_urls = True

        if processed_all_urls == True:
            break


# Close the driver after processing all URLs
driver.quit()
print("All URLs processed. Driver closed.")


#sys.exit()



#Basic DB Function
def get_data_from_csv(location, drop_col = None):
    if drop_col:
        df = pd.read_csv(location)
        df = df.drop([drop_col], axis = 1)
    else:
        df = pd.read_csv(location)
    return df



def execute_select_query(engine, query):
    """
    주어진 SQLAlchemy 엔진과 SQL 쿼리를 사용하여 쿼리를 실행하고 결과를 데이터프레임으로 반환하는 함수.
    :param engine: SQLAlchemy 엔진 객체
    :param query: 실행할 SQL 쿼리 문자열
    :return: 쿼리 결과를 포함하는 pandas DataFrame
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        df = pd.DataFrame(result.fetchall(), columns=result.keys())
    return df


def execute_query(engine, query):
    """
    주어진 SQLAlchemy 엔진과 SQL 쿼리를 사용하여 쿼리를 실행하고 결과를 데이터프레임으로 반환하는 함수.
    :param engine: SQLAlchemy 엔진 객체
    :param query: 실행할 SQL 쿼리 문자열
    :return: 쿼리 결과를 포함하는 pandas DataFrame
    """
    with engine.connect() as connection:
        connection.execute(text(query))


def execute_insert_query(engine, df, table_name):
    """
    주어진 SQLAlchemy 엔진과 데이터프레임을 사용하여 테이블에 데이터를 삽입하는 함수.
    :param engine: SQLAlchemy 엔진 객체
    :param df: 삽입할 데이터프레임
    :param table_name: 데이터가 삽입될 테이블 이름
    """
    with engine.connect() as connection:
        # 데이터프레임의 각 행을 사전으로 변환
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

        print(f"{df.shape[0]} rows has been successfully inserted into the '{table_name}' table.")



# AWS Connection
# AWS RDS MySQL 데이터베이스 접속 정보
db_host = 'mydnovadb.c7u0am6wacri.ap-northeast-2.rds.amazonaws.com'
db_name = 'YTDB'
db_user = 'mydnovadb'
db_password = 'dnova998877'
db_port = '3306'

# SQLAlchemy 엔진 생성
engine = create_engine(f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')



# Basic Query
"""
query = 'TRUNCATE SHORTS_INFO'
x = execute_query(engine,query)


query = 'SELECT * FROM SHORTS_INFO'
#query = 'TRUNCATE SHORTS_INFO'

x = execute_select_query(engine,query)
"""

# Save to AWS
df_to_insert = get_data_from_csv(csv_file,'is_posted_in_date_range')
table_name = 'SHORTS_INFO'
execute_insert_query(engine,df_to_insert,table_name)

print(datetime.now())