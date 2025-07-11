# StreetLight Data API – Automated AADT Analysis Using OSM IDs

Automate StreetLight Data’s API workflow to extract **Annual Average Daily Traffic (AADT)** for custom OpenStreetMap (OSM) road segments.

This repository provides robust Python scripts, clear documentation, and best practices for:

- Building custom zone sets from OSM segment IDs
- Submitting and tracking AADT analyses
- Handling API status and download endpoints
- Downloading results as CSV/shapefile and organizing outputs
- Troubleshooting the full process

---

## 🚗 Background & Motivation

StreetLight Data offers advanced mobility analytics, but its API is multi-step and requires careful sequencing.  
This project was built through hands-on problem solving with the following challenges:

- **Challenge:** The API process is multi-step, with dependencies at each stage.
  - **Solution:** Scripts are organized to follow the API logic (zone set creation → analysis submission → status polling → results download).
- **Challenge:** OSM IDs must be correctly sourced, deduplicated, and managed.
  - **Solution:** This README explains how to obtain and manage OSM IDs, and the scripts handle input lists or batches.
- **Challenge:** Results (metrics) are only available after analysis completion, and metric names may differ.
  - **Solution:** The status-checking script reveals available metrics before downloading, and the download code uses only verified metric names.

---

## 🌍 Where Do OSM IDs Come From? How Do I Manage Them?

**OpenStreetMap (OSM) segment IDs** uniquely identify road line features.

**How to extract OSM IDs:**

- **QGIS or ArcGIS:**  
  - Import OSM line data (e.g., from [Geofabrik](https://download.geofabrik.de/)), select your area, and export the `osm_id` field from your selection.
- **Overpass Turbo:**  
  - Use [overpass-turbo.eu](https://overpass-turbo.eu/), run a line/way query, and export features. Extract OSM IDs from the GeoJSON or CSV output.
- **Python OSM Libraries:**  
  - Use [osmnx](https://osmnx.readthedocs.io/) or [osmapi](https://pypi.org/project/OsmApi/) to query and parse OSM data, then save the line segment IDs.

**Tips:**
- Always deduplicate your list and ensure you use only **line feature IDs** (not nodes or polygons).
- Save OSM IDs as a Python list, CSV, or text file. For large projects, process in batches of ≤500 IDs per API request (the StreetLight API limit).

---

## 🛠️ Workflow Summary

1. **Create a Zone Set:**  
   Submit your OSM IDs to StreetLight; receive a `zone_set_uuid`.

2. **Submit an AADT Analysis:**  
   Reference your zone set, select year, travel mode, and parameters.

3. **Poll for Analysis Status:**  
   Wait for job status to be “Available” (or “completed”).

4. **Check Available Metrics:**  
   Each analysis may expose unique metrics (`aadt`, `estimated_aadt`, etc.).

5. **Download Results:**  
   Download CSV (tabular) and/or shapefile (GIS) results.

---

## 🐍 Example Usage

### 1. Create a Zone Set from OSM IDs

```python
import requests

API_KEY = "YOUR_API_KEY"
INSIGHT_LOGIN_EMAIL = "your@email.com"
osm_ids = [15373817, 15373820, 15373822]  # Your OSM line IDs

zone_set_url = f"https://insight.streetlightdata.com/api/v2/zone_sets?key={API_KEY}"
zone_set_payload = {"osm_ids": osm_ids, "insight_login_email": INSIGHT_LOGIN_EMAIL}
headers = {"accept": "application/json", "content-type": "application/json"}

response = requests.post(zone_set_url, json=zone_set_payload, headers=headers)
zone_set_uuid = response.json()["uuid"]
print("Zone Set UUID:", zone_set_uuid)
