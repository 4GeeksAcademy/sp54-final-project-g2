
import requests
import json

client_id = '4168-7_MECuFfEInQfI3RvfnSzbPLINZcfbcH2mmzHDFwGKnZJrfG1czC'
client_secret = 'oUHsYodoVSa51ijaG4aIZCLp9izXvlV3Xsor4ujr6EltJG4aSV'
url = 'https://interface-test.g-stock.net/external/api/auth'


@app.route('https://interface.g-stock.net/external/api/auth', methods = ['POST'])
def auth():
    client_id = '4168-8_GyDu3BUnxExvpLNrm0k79bnJfK6PxdzM3VKPKjJNxvkrnu6Ygv'
    client_secret = 'f9Vhjeg5rGuiwdeYxRXRwUjFafEQD3LhTZzKnn1X8UovuOdfLn'
    if None in [client_id, client_secret]:
        return json.dumps({"error": "invalid_request"}), 400
