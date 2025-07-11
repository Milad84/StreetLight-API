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

url = "https://insight.streetlightdata.com/api/v2/debug/echo?key=YOUR API KEY"

payload = { "message": "hello worlddddd" }
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)