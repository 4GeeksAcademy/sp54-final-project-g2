
import requests
import json

url = os.environ.get('URL_GS')
client_id = os.environ.get('CLIENT_COB')
client_secret = os.environ.get('SECRET_COB')

payload = json.dumps({
    "client_id": client_id,
    "client_secret": client_secret
})
headers = {
    'Content-Type': 'application/json'
}

response = requests.request("POST", url , headers=headers, data=payload)

print(response.text)
