import requests

url = "https://insight.streetlightdata.com/api/v2/zone_sets?key=0PquI2MHeFd17nWNwxBSf1oj4LnhozdU"

payload = {
    "osm_ids": [15373817],
    "insight_login_email": "milad.mohammadalizadehkorde@austintexas.gov"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)