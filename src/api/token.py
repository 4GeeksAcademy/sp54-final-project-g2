
import requests
import json

client_id = '4168-7_MECuFfEInQfI3RvfnSzbPLINZcfbcH2mmzHDFwGKnZJrfG1czC'
client_secret = 'oUHsYodoVSa51ijaG4aIZCLp9izXvlV3Xsor4ujr6EltJG4aSV'
url = 'https://interface-test.g-stock.net/external/api/auth'

def auth():
    payload = json.dumps  ({"client_id": client_id,
                            "client_secret": client_secret})
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", {url}, headers=headers, data=payload)
    print(response.text)

    '''if None in [client_id, client_secret]:
        return json.dumps({"error": "invalid_request"}), 400
    if not authenticate_client(client_id, client_secret):
        return json.dumps({"error": "invalid_client"}), 400
    access_token = generate_access_token()
    return json.dumps ({"access_token": access_token,
                        "token_type": "JWT",
                        "expires_in": LIFE_SPAN})'''
