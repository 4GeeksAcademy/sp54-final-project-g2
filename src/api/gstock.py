from flask import request


def get_token_access(client_id, client_secret):
    url_token = 'https://interface-test.g-stock.net/external/api/token'
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }

    try:
        answer = requests.post(url_token, data=payload)
        if answer.status_code == 200:
            token_acceso = answer.json().get('access_token')
            return token_acceso
        else:
            print(f"Error al obtener el token de acceso: {answer.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_request_api(url, token_acceso):
    headers = {
        'Authorization': f'Bearer {token_acceso}',
        'Content-Type': 'application/json'
    }
    try:
        answer = requests.get(url, headers=headers)
        if answer.status_code == 200:
            return answer.json()
        else:
            print(f"Error al hacer la solicitud autenticada: {answer.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Credenciales de cliente OAuth2
client_id = '4168-7_MECuFfEInQfI3RvfnSzbPLINZcfbcH2mmzHDFwGKnZJrfG1czC'
client_secret = 'oUHsYodoVSa51ijaG4aIZCLp9izXvlV3Xsor4ujr6EltJG4aSV'

# Obtener token de acceso
token = get_token_access(client_id, client_secret)
if token:
    # URL del recurso protegido
    url = 'https://interface-test.g-stock.net/external/api/auth'
    # Hacer solicitud autenticada
    datos = get_request_api(url, token)
    if datos:
        print("Solicitud autenticada exitosa.")
        print(datos)