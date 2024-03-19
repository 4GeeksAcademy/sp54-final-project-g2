from flask import Flask, request, jsonify, url_for, Blueprint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


@app.route('https://interface-test.g-stock.net/external/api/auth', methods = ['POST'])
def auth():
    client_id = '4168-7_MECuFfEInQfI3RvfnSzbPLINZcfbcH2mmzHDFwGKnZJrfG1czC'
    client_secret = 'oUHsYodoVSa51ijaG4aIZCLp9izXvlV3Xsor4ujr6EltJG4aSV'
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