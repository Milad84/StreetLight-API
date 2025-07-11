import requests
import json

API_KEY = "0PquI2MHeFd17nWNwxBSf1oj4LnhozdU"
ANALYSIS_UUID = "6ae27872-9a0a-49de-a0bf-bba7601d1144"

status_url = f"https://insight.streetlightdata.com/api/v2/analyses/status?key={API_KEY}"
payload = { "analyses": [{ "uuid": ANALYSIS_UUID }] }
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(status_url, json=payload, headers=headers)
status_json = response.json()
print(json.dumps(status_json, indent=2))
