import requests
import os

API_KEY = "0PquI2MHeFd17nWNwxBSf1oj4LnhozdU"
ANALYSIS_UUID = "6ae27872-9a0a-49de-a0bf-bba7601d1144"
METRIC = "estimated_aadt"

# --- Prompt user for save folder ---
save_dir = input("Enter the full path to the folder where you want to save the CSV: ").strip()
if not save_dir:
    save_dir = "."  # Default to current directory

os.makedirs(save_dir, exist_ok=True)

download_url = (
    f"https://insight.streetlightdata.com/api/v2/analyses/download/uuid/"
    f"{ANALYSIS_UUID}/{METRIC}?key={API_KEY}"
)

headers = {"accept": "text/csv"}
response = requests.get(download_url, headers=headers)

if response.status_code == 200:
    filename = f"{ANALYSIS_UUID}_{METRIC}.csv"
    filepath = os.path.join(save_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"✅ Downloaded as {filepath}")
else:
    print(f"❌ Failed to download CSV. Status: {response.status_code}")
    print(response.text)
