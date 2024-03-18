"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


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
        return jsonify({"msg": "The email already exist"}), 400

    # Crear un nuevo usuario
    new_user = User(email = data['email'],
                    rol = "Jefe cocina",
                    password = data['password'],
                    is_active = True)

    db.session.add(new_user)    
    db.session.commit()

    # Crear un token de acceso para el nuevo usuario
    access_token = create_access_token(identity=new_user.id)

    response_body['msg'] = "User resgistered succesfull"
    return jsonify({"token": access_token, "user_id": new_user.id}), 201


# ENDPOINT para consultar o dar de alta una linea de albaran GET o POST
@api.route("/delivery_note_lines/<int:delivery_note>", methods['GET', 'POST'])
def handle_delivery_lines(user_id, delivery_note_id): # se tiene que filtrar por usuario y numero de albaran
    response_body = {}
    results = []

    if request.method == 'GET':
        line = delivery_note_lines.query.filter_by(user_id = user_id, delivery_note_id = delivery_note_id).scalars()
        response_body['results'] = [row.serialize() for row in line]
        response_body['message'] = 'GET Method Delivery Note Line'
        return response_body, 200

    if request.method == 'POST':
        data = request.json
        line = DeliveryNoteLines (  qty = data['qty'],
                                    unit_cost = data['unit_cost'], # este campo deberia de venir de la tabla Recipes
                                    total = data['total'],
                                    vat = data['vat'],
                                    recipe_id = data['recipe_id'], # este campo deberia de venir de la tabla Recipes
                                    delivery_note_id = data['delivery_note_id'],) # este campo deberia de venir de la tabla DeliveryNotes
        db.session.add(line)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = 'POST Method Delivery Note Line'
        return response_body, 200


# ENDPOINT para poder editar o borrar una linea del albaran PUT o DELETE
@api.route("/delivery_note_lines/<int:user_id>/delivery_line/<int:delivery_note_line_id>", methods=['DELETE', 'PUT'])
def modify_delivery_lines(user_id, delivery_note_lines_id):
    response_body = {}
    results = []

    if request.method == 'DELETE':
        line = delivery_note_lines_id.query.filter_by(user_id = user_id, delivery_note_lines_id = delivery_note_lines_id).first()
        if line:
            db.session.delete(line)
            db.session.commit()
            response_body['message'] = f'Delivery Note Line {delivery_note_line_id} del usuario {user_id} ha sido eliminada'
            return response_body, 200
        else:
            response_body['message'] = f'No se ha podido borrar la linea {delivery_note_line_id}'
            return response_body, 401

    if request.method == 'PUT':
        line = delivery_note_lines_id.query.filter_by(user_id = user_id, delivery_note_lines_id = delivery_note_lines_id).first()
        if not line:
            response_body['message'] = f'No se ha encontrado la linea {delivery_note_line_id}'
            return response_body, 404
        data = request.json
        line = DeliveryNoteLines (  qty = data['qty'],
                                    total = data['total'],
                                    vat = data['vat'],)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = f'Delivery Note Line {delivery_note_line_id} se ha actualizado con exito'
        return response_body, 200


if __name__ == '__main__':
    app.run(debug=True)
#







