"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users
"""from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required"""


api = Blueprint('api', __name__)
CORS(api)  # Allow CORS requests to this API


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {}
    response_body['message'] = "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    return response_body, 200


@api.route("/login", methods=["POST"])
def create_token():
    response_body = {}
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    rol = request.json.get("rol", None)
    user = db.session.query(Users).filter(email=email, password=password, rol=rol).first()
    if user is None:
        return jsonify({"msg": "Acces denied"}), 401
    access_token = create_access_token(identity = user.id)
    response_body["msg"] = "Welcome"
    return jsonify({ "token": access_token, "user_id": user.id }), 200       


@api.route("/register", methods["POST"])
def register_user():
    response_body = {}
    data = request.json

    # Verificar si el email ya existe.
    existing_user = User.query.filter_by(email=data['email']).first()    
    if existing_user:
        return jsonify({"msg": "The eMail already exist"}), 400

    # Crear un nuevo usuario
    new_user = User(
        email=data['email'],
        rol="Jefe cocina",
        password=data['password'],
        is_active=True)

    db.session.add(new_user)    
    db.session.commit()

    # Crear un token de acceso para el nuevo usuario
    access_token = create_access_token(identity=new_user.id)

    response_body['msg'] = "User resgistered succesfull"
    return jsonify({"token": access_token, "user_id": new_user.id}), 201


if __name__ == '__main__':
    app.run(debug=True)








