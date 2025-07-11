import requests

url = "https://insight.streetlightdata.com/api/v2/zone_sets?key=YOUR API KEY"

payload = {
    "osm_ids": [15373817],
    "insight_login_email": "YOUR LOGIN EMAIL"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)