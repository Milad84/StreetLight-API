import requests

url = "https://insight.streetlightdata.com/api/v2/analyses/download/uuid/6ae27872-9a0a-49de-a0bf-bba7601d1144/analysis_line?key=0PquI2MHeFd17nWNwxBSf1oj4LnhozdU"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)