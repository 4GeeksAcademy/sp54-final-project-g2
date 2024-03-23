
import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()

# Variables ocultas
url = os.getenv("URL_GS")
client_id_cob = os.getenv("CLIENT_COB")
client_secret_cob = os.getenv("SECRET_COB")
url_base = os.getenv("URL_GS_BS")

# Obtengo el token
payload = json.dumps({"client_id": client_id_cob, "client_secret": client_secret_cob})
headers = {'Content-Type': 'application/json'}

response = requests.request("POST", url , headers=headers, data=payload)

# Destructuro la respuesta JSON
if response.status_code == 200:
    json_response = response.json()
    access_token = json_response.get("access_token") # Almaceno el token en una variable
    center = json_response.get("center")
    user_centers = json_response.get("userCenters")
    if user_centers:
        for center in user_centers:
            center_id = center.get("id")
            center_name = center.get("name")
    if access_token:
        print("Access Token:", access_token)
        print("Center:" , center_id, 'Nombre:', center_name )
    else:
        print("No se encontró el Token en la respuesta JSON.")
else:
    print("Error al enviar la solicitud:", response.status_code)

# Obtener categorias de productos
headers = {'Authorization': f'Bearer {access_token}'}
category = requests.get(url_base + 'v1/product/purchases/categories', headers=headers)

print(category.json())
