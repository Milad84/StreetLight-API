import requests

url = "https://insight.streetlightdata.com/api/v2/analyses/download/uuid/6ae27872-9a0a-49de-a0bf-bba7601d1144/analysis_line?key=YOUR API KEY"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)