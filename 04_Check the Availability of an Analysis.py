import requests

url = "https://insight.streetlightdata.com/api/v2/analyses/status?key=YOUR API KEY"

payload = { "analyses": [{ "uuid": "6ae27872-9a0a-49de-a0bf-bba7601d1144" }] }
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)