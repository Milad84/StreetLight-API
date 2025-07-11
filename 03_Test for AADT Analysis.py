#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      MohammadalizadehkorM
#
# Created:     10/07/2025
# Copyright:   (c) MohammadalizadehkorM 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import requests

API_KEY = "0PquI2MHeFd17nWNwxBSf1oj4LnhozdU"
INSIGHT_LOGIN_EMAIL = "milad.mohammadalizadehkorde@austintexas.gov"

# 1. Create Zone Set from OSM IDs
ZONE_SET_URL = f"https://insight.streetlightdata.com/api/v2/zone_sets?key={API_KEY}"
zone_set_payload = {
    "osm_ids": [
        15373817, 15373820, 15373822, 15373983, 15374346, 15374867,
        15375075, 15375257, 15376678, 15376768, 15376868, 15377471, 15377534
    ],
    "insight_login_email": INSIGHT_LOGIN_EMAIL
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

print("Creating zone set from OSM IDs...")
zone_set_response = requests.post(ZONE_SET_URL, json=zone_set_payload, headers=headers)
zone_set_data = zone_set_response.json()
zone_set_uuid = zone_set_data["uuid"]
print("Zone Set UUID:", zone_set_uuid)

# 2. Submit the AADT Analysis
ANALYSIS_URL = f"https://insight.streetlightdata.com/api/v2/analyses?key={API_KEY}"
analysis_payload = {
    "analysis_type": "AADT",
    "travel_mode_type": "All_Vehicles_LBS_Plus",
    "day_parts": "All Day|0023,Early AM|0005,Peak AM|0609,Mid-Day|1014,Peak PM|1518,Late PM|1923",
    "day_types": "Weekday|14,Weekend Day|67,All Days|17",
    "metric_type": "segment",
    "insight_login_email": INSIGHT_LOGIN_EMAIL,
    "analysis_name": "osm_id_Test",
    "description": "AADT for OSM-based zone set",
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
print("Submitting AADT analysis...")
analysis_response = requests.post(ANALYSIS_URL, json=analysis_payload, headers=headers)
print("Analysis response:")
print(analysis_response.text)
