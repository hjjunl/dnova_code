# import os
# import pandas as pd

# # Define the initial path where the revised files are located
# initial_path = "C:/Users/HyunJunLee/Documents/hj_git/YouTube_Report_Automation/YouTube_Shorts_Automation/youtube_shorts_crawling/change_fixced url copy/change_fixced url copy/"
# revised_folder = os.path.join(initial_path, "revised")

# # List to hold all the dataframes from individual Excel files
# df_list = []

# # Loop through all files in the revised_folder directory
# for file_name in os.listdir(revised_folder):
#     # Check if the file name starts with 'revised_url' and ends with '.xlsx'
#     if file_name.startswith("revised_url") and file_name.endswith(".xlsx"):
#         file_path = os.path.join(revised_folder, file_name)
#         print(f"Reading file: {file_path}")  # Print file being read for tracking
#         # Read each Excel file and append it to the dataframe list
#         df = pd.read_excel(file_path)
#         df_list.append(df)

# # Concatenate all dataframes into one
# combined_df = pd.concat(df_list, ignore_index=True)

# # Save the combined dataframe to a new Excel file in the initial path
# combined_output_path = os.path.join(initial_path, "combined_revised_urls.xlsx")
# combined_df.to_excel(combined_output_path, index=False)

# print(f"Combined Excel file saved to: {combined_output_path}")








# import pandas as pd
# import os

# # Define file paths
# initial_path = "C:/Users/HyunJunLee/Documents/hj_git/YouTube_Report_Automation/YouTube_Shorts_Automation/youtube_shorts_crawling/change_fixced url copy/change_fixced url copy/"
# youtube_data_file = os.path.join(initial_path, "Youtube_Data_2024-05-14.xlsx")
# combined_revised_file = os.path.join(initial_path, "combined_revised_urls.xlsx")

# # Read the two Excel files
# youtube_data_df = pd.read_excel(youtube_data_file)
# combined_revised_df = pd.read_excel(combined_revised_file)

# # Print columns of both DataFrames for verification
# print("Columns in YouTube Data DataFrame:", youtube_data_df.columns)
# print("Columns in Combined Revised DataFrame:", combined_revised_df.columns)

# # Rename 'yt_title' in the combined_revised_df to 'channel_name' to match the youtube_data_df
# combined_revised_df = combined_revised_df.rename(columns={'yt_title': 'channel_name'})

# # Merge the dataframes using 'channel_name' as the common key
# merged_df = pd.merge(youtube_data_df, combined_revised_df[['channel_name', 'yt_url']], on='channel_name', how='left')

# # Rename the 'yt_url' column to 'fixed_shorts_url' in the merged DataFrame
# merged_df = merged_df.rename(columns={'yt_url': 'fixed_shorts_url'})

# # Save the merged dataframe to a new Excel file
# merged_output_path = os.path.join(initial_path, "merged_youtube_data.xlsx")
# merged_df.to_excel(merged_output_path, index=False)

# print(f"Merged Excel file saved to: {merged_output_path}")


# import pandas as pd
# import os

# # 파일 경로 설정
# initial_path = "C:/Users/HyunJunLee/Documents/hj_git/YouTube_Report_Automation/YouTube_Shorts_Automation/youtube_shorts_crawling/change_fixced url copy/change_fixced url copy/"
# input_file = os.path.join(initial_path, "merged_youtube_data.xlsx")  # 기존 엑셀 파일명
# output_file = os.path.join(initial_path, "us_korea_test.xlsx")  # 결과 엑셀 파일명

# # 엑셀 파일 읽기
# df = pd.read_excel(input_file)

# # 필터링 조건: country가 'United States' 또는 'South Korea'이며, 'yt_rul_y' 컬럼이 빈값이 아닌 경우
# filtered_df = df[(df['country'].isin(['United States', 'South Korea'])) & (df['yt_url_y'].notna())]

# # 필터링된 결과를 새로운 엑셀 파일로 저장
# filtered_df.to_excel(output_file, index=False)

# print(f"Filtered Excel file saved to: {output_file}")

import requests
import re
# Define the payload and headers for the request
API_KEY = '3397e8a6a37e89b03b08750a27575df8'
payload = {
    'api_key': API_KEY,
    'url': 'https://www.youtube.com/watch?v=xEuH_5Ik92U'
}

headers = {
    'x-sapi-render': 'true',
    'x-sapi-instruction_set': '[{"type":"scroll","direction":"y","value":"bottom"}]'
}

# Make the GET request
r = requests.get('https://api.scraperapi.com/', params=payload, headers=headers, verify=False)

# Save the response text to a file
with open('response_output.txt', 'w', encoding='utf-8') as file:
    file.write(r.text)

print("Response saved to response_output.txt")
