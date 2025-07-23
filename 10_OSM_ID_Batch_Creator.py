#-------------------------------------------------------------------------------
# Name:        streetlight_batch_submit
# Purpose:     Clean up existing zone sets, chunk unique OSM IDs, submit AADT analyses, log UUIDs
#-------------------------------------------------------------------------------

import os
import sys
import requests
import time
import json
import pandas as pd

# --------- Set working directory to script location ---------
target_dir = r"G:\ATD\ACTIVE TRANS\Vision Zero\GIS\StreetLight"
os.chdir(target_dir)
print("Changed working directory to:", os.getcwd(), flush=True)

# --------- Import your OSM ID list from OSM_id_list_AFP.py ---------
try:
    from OSM_id_list_AFP import osm_id_list
    print("Imported", len(osm_id_list), "OSM IDs from OSM_id_list_AFP.py", flush=True)
except ModuleNotFoundError as e:
    print("ERROR: Could not import 'OSM_id_list_AFP.py'.", flush=True)
    print("Make sure the file is named exactly 'OSM_id_list_AFP.py' and is in this folder:", os.getcwd(), flush=True)
    sys.exit(1)
except Exception as e:
    print(f"ERROR: Could not import OSM IDs: {e}", flush=True)
    sys.exit(1)

# --------- API keys and endpoints ---------
API_KEY = "YOUR API KEY"
INSIGHT_LOGIN_EMAIL = "YOUR EMAIL"

ZONE_SET_URL = f"https://insight.streetlightdata.com/api/v2/zone_sets?key={API_KEY}"
ZONE_LIST_URL = f"https://insight.streetlightdata.com/api/v2/zone_sets?key={API_KEY}"
ZONE_DELETE_URL = f"https://insight.streetlightdata.com/api/v2/zone_sets/{{zone_uuid}}?key={API_KEY}"
ANALYSIS_URL = f"https://insight.streetlightdata.com/api/v2/analyses?key={API_KEY}"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json"
}

# --------- Clean up existing zones ---------
def cleanup_existing_zones():
    print("\n--- Cleaning up existing zone sets for your API key ---", flush=True)
    try:
        resp = requests.get(ZONE_LIST_URL, headers=HEADERS, timeout=60)
        if resp.status_code == 200:
            zone_data = resp.json()
            if "zone_sets" in zone_data:
                zones = zone_data["zone_sets"]
                print(f"Found {len(zones)} existing zones.", flush=True)
                deleted = 0
                for z in zones:
                    uuid = z.get("uuid")
                    if uuid:
                        del_url = ZONE_DELETE_URL.format(zone_uuid=uuid)
                        dresp = requests.delete(del_url, headers=HEADERS, timeout=60)
                        if dresp.status_code == 200:
                            deleted += 1
                            print(f"Deleted zone {uuid}", flush=True)
                        else:
                            print(f"Failed to delete zone {uuid}: {dresp.text}", flush=True)
                        time.sleep(0.3)  # Avoid API throttling
                print(f"Deleted {deleted} zones.", flush=True)
            else:
                print("No 'zone_sets' key found in zone list response.", flush=True)
        else:
            print(f"Failed to list zones: {resp.text}", flush=True)
    except Exception as e:
        print(f"Error during zone cleanup: {e}", flush=True)

cleanup_existing_zones()

# --------- Chunking function (no duplicates, original order preserved) ---------
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

batch_size = 500
max_retries = 3
zone_set_uuids = []
analysis_uuids = []
failed_batches = []

# --------- Main batch processing loop with retry logic ---------
for idx, batch in enumerate(chunks(osm_id_list, batch_size), 1):
    print(f"\n---- Processing Batch {idx} ----", flush=True)

    # STEP 1: Create Zone Set for this batch of OSM IDs (with retries)
    zone_set_uuid = None
    for attempt in range(max_retries):
        zone_set_payload = {
            "osm_ids": batch,
            "insight_login_email": INSIGHT_LOGIN_EMAIL
        }
        print(f"Creating zone set for Batch {idx} (attempt {attempt+1}, {len(batch)} OSM IDs)...", flush=True)
        try:
            zone_set_response = requests.post(ZONE_SET_URL, json=zone_set_payload, headers=HEADERS, timeout=60)
            zone_set_data = zone_set_response.json()
            print("Zone Set Response:", zone_set_data, flush=True)
            if "uuid" in zone_set_data:
                zone_set_uuid = zone_set_data["uuid"]
                zone_set_uuids.append(zone_set_uuid)
                print(f"Zone Set UUID for Batch {idx}: {zone_set_uuid}", flush=True)
                break  # Success!
            elif 'message' in zone_set_data:
                print(f"Error in zone set for Batch {idx}: {zone_set_data['message']}", flush=True)
            else:
                print(f"Unknown error or format in zone set for Batch {idx}", flush=True)
        except Exception as e:
            print(f"Error in zone set POST for Batch {idx} attempt {attempt+1}: {e}", flush=True)
        time.sleep(2)  # Wait before retry

    # If still no uuid after retries, log and skip
    if not zone_set_uuid:
        print(f"ERROR: Failed to create zone set for Batch {idx} after {max_retries} attempts. Skipping batch.", flush=True)
        failed_batches.append({'batch': idx, 'reason': 'zone_set_failed'})
        continue

    # STEP 2: Submit AADT Analysis for this zone set (with retries)
    analysis_uuid = None
    for attempt in range(max_retries):
        analysis_name = f"osm_analysis_{idx:03}"
        analysis_payload = {
            "analysis_type": "AADT",
            "travel_mode_type": "All_Vehicles_LBS_Plus",
            "day_parts": "All Day|0023,Early AM|0005,Peak AM|0609,Mid-Day|1014,Peak PM|1518,Late PM|1923",
            "day_types": "Weekday|14,Weekend Day|67,All Days|17",
            "metric_type": "segment",
            "insight_login_email": INSIGHT_LOGIN_EMAIL,
            "analysis_name": analysis_name,
            "description": f"AADT for OSM-based zone set batch {idx}",
            "date_ranges": [
                {
                    "start_date": "01/01/2024",
                    "end_date": "12/31/2024"
                }
            ],
            "oz_sets": [
                {"uuid": zone_set_uuid}
            ],
            "aadt_year": 2024,
            "unit_of_measurement": "miles",
            "enable_visualization": True
        }
        print(f"Submitting AADT analysis for Batch {idx} (attempt {attempt+1})...", flush=True)
        try:
            analysis_response = requests.post(ANALYSIS_URL, json=analysis_payload, headers=HEADERS, timeout=60)
            analysis_data = analysis_response.json()
            print("Analysis Response:", analysis_data, flush=True)
            if "uuid" in analysis_data:
                analysis_uuids.append({
                    "batch": idx,
                    "zone_set_uuid": zone_set_uuid,
                    "analysis_uuid": analysis_data["uuid"],
                    "analysis_name": analysis_name
                })
                print(f"Analysis UUID for Batch {idx}: {analysis_data['uuid']}", flush=True)
                analysis_uuid = analysis_data["uuid"]
                break  # Success!
            elif 'message' in analysis_data:
                print(f"Error in analysis for Batch {idx}: {analysis_data['message']}", flush=True)
            else:
                print(f"Unknown error or format in analysis for Batch {idx}", flush=True)
        except Exception as e:
            print(f"Error in analysis POST for Batch {idx} attempt {attempt+1}: {e}", flush=True)
        time.sleep(2)  # Wait before retry

    # If still no analysis uuid after retries, log and skip
    if not analysis_uuid:
        print(f"ERROR: Failed to submit analysis for Batch {idx} after {max_retries} attempts.", flush=True)
        failed_batches.append({'batch': idx, 'reason': 'analysis_failed'})

    # STEP 3: Rate limiting delay
    time.sleep(1)  # Increase if you get API rate limit errors

# --------- Save mapping for analysis download (JSON + CSV) ---------
print("\n--- All Batches Processed ---", flush=True)
print("Zone Set UUIDs:", zone_set_uuids, flush=True)
print("Analysis UUIDs and Names:", flush=True)
for a in analysis_uuids:
    print(a, flush=True)

# Save mapping to JSON
with open("analysis_uuid_log.json", "w") as f:
    json.dump(analysis_uuids, f, indent=2)
# Save mapping to CSV
pd.DataFrame(analysis_uuids).to_csv("analysis_uuid_log.csv", index=False)

if failed_batches:
    print("\nSome batches failed:", failed_batches, flush=True)
    with open("failed_batches_log.json", "w") as f:
        json.dump(failed_batches, f, indent=2)
else:
    print("\nAll batches processed successfully!", flush=True)

print("\nAnalysis-to-batch mapping saved to 'analysis_uuid_log.json' and 'analysis_uuid_log.csv'.", flush=True)
print("\nScript finished!", flush=True)
