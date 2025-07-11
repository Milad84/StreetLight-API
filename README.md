# StreetLight-API 
Python tools for automating StreetLight Data API AADT analysis using OSM segment IDs. Create zone sets, submit analyses, monitor status, and download AADT results (CSV/shapefile). Includes full example scripts and workflow documentation.

# StreetLight Data API – Automated AADT Analysis and Results Download

Automate the extraction of Annual Average Daily Traffic (AADT) metrics from the StreetLight Data API for custom OSM street segments.  
This repo contains Python scripts and workflow documentation for:

- Creating zone sets from OpenStreetMap (OSM) line segment IDs
- Submitting AADT analyses and monitoring status
- Checking available result metrics
- Downloading results in CSV or shapefile format to a local directory

---

## 🚦 Features

- **Zone Set Creation:** Group your OSM segments for analysis
- **AADT Analysis Submission:** Automate configuration and launch of AADT runs
- **Status Monitoring:** Poll API for completion and available result types
- **Automated Results Download:** Get your data as CSV or shapefile, in a folder of your choice
- **Ready-to-use Python Scripts:** Modular and documented for easy adaptation

---

## 📦 Requirements

- Python 3.x  
- [`requests`](https://pypi.org/project/requests/) library  
- StreetLight API Key and login email  
- List of OSM segment IDs (as integers)

---

## ⚡️ Quick Start

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```
2. **Install dependencies**
    ```bash
    pip install requests
    ```
3. **Edit the example scripts**
    - Add your StreetLight API Key, email, and OSM IDs where indicated.

4. **Run the scripts**
    - Follow the prompts to save output files.
    - Open downloaded CSVs or shapefiles in your preferred tool.

---

## 📝 Example Usage

```python
import requests

API_KEY = "YOUR_API_KEY"
ANALYSIS_UUID = "your_analysis_uuid"
METRIC = "estimated_aadt"
save_dir = input("Enter folder path to save the CSV: ").strip()
if not save_dir:
    save_dir = "."

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
    print(f"Downloaded as {filepath}")
else:
    print(f"Failed to download CSV. Status: {response.status_code}")
    print(response.text)
