from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


@app.route('https://interface.g-stock.net/external/api/auth', methods = ['POST'])
def auth():
    client_id = '4168-8_GyDu3BUnxExvpLNrm0k79bnJfK6PxdzM3VKPKjJNxvkrnu6Ygv'
    client_secret = 'f9Vhjeg5rGuiwdeYxRXRwUjFafEQD3LhTZzKnn1X8UovuOdfLn'
    if None in [client_id, client_secret]:
        return json.dumps({
        "error": "invalid_request"
        }), 400
    if not authenticate_client(client_id, client_secret):
        return json.dumps({
        "error": "invalid_client"
        }), 400
    access_token = generate_access_token()
    return json.dumps({ 
    "access_token": access_token,
    "token_type": "JWT",
    "expires_in": LIFE_SPAN
    })