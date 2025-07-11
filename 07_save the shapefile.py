#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      MohammadalizadehkorM
#
# Created:     10/07/2025
# Copyright:   (c) MohammadalizadehkorM 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import requests
import os

API_KEY = "0PquI2MHeFd17nWNwxBSf1oj4LnhozdU"
ANALYSIS_UUID = "6ae27872-9a0a-49de-a0bf-bba7601d1144"
DOWNLOAD_URL = (
    f"https://insight.streetlightdata.com/api/v2/analyses/download/uuid/"
    f"{ANALYSIS_UUID}/analysis_line?key={API_KEY}"
)

headers = {"accept": "application/json"}

print("Checking for shapefile download URL...")
response = requests.get(DOWNLOAD_URL, headers=headers)

content_type = response.headers.get("Content-Type", "")
filename = "streetlight_analysis_shapefile.zip"

# Ask the user for a download folder
save_dir = input("Enter a folder to save the file (leave blank for current directory): ").strip()
if save_dir:
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, filename)

if "application/json" in content_type:
    try:
        result = response.json()
        print("JSON response:", result)
        download_url = (
            result.get("download_url")
            or result.get("url")
            or result.get("shapefile_url")
        )
        if not download_url:
            print("No download URL found in the response!")
            exit(1)
        print("Found download URL:", download_url)
        file_response = requests.get(download_url)
        if file_response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(file_response.content)
            print(f"Shapefile downloaded as {filename}")
        else:
            print("Failed to download the file. Status code:", file_response.status_code)
            print(file_response.text)
    except Exception as e:
        print("Error parsing JSON or downloading file:", e)
elif "application/zip" in content_type or "application/octet-stream" in content_type:
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Shapefile downloaded directly as {filename}")
else:
    print("Response is not JSON or a ZIP file. Content-Type:", content_type)
    print("Raw response:", response.text)
