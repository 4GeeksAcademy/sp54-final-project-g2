import json
import requests

payload = json.dumps({
    "client_id": "4168-7_MECuFfEInQfI3RvfnSzbPLINZcfbcH2mmzHDFwGKnZJrfG1czC",
    "client_secret": "oUHsYodoVSa51ijaG4aIZCLp9izXvlV3Xsor4ujr6EltJG4aSV"
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", {"https://interface-test.g-stock.net/external/api/auth"}, headers=headers, data=payload)

print(response.text)
