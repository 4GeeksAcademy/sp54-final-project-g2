"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, Centers, Compositions, Recipes, Supliers, References, Previsions, DeliveryNotes, DeliveryNoteLines, CompositionLines, LineRecipes, ManufacturingOrders
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
    user = db.session.query(Users).filter(Users.email==email, Users.password==password, Users.rol==rol).first()
    if user is None:
        response_body['message'] = "Access denied"
        return response_body, 401
    access_token = create_access_token(identity = {'user_id': user.id, 'rol': user.rol})
    response_body['message'] = "Welcome"
    response_body['token'] = access_token
    response_body['user'] = user.serialize()
    return response_body, 200       


@api.route("/register", methods=["POST"])
def register_user():
    response_body = {}
    data = request.json
    if "email" not in data:
        response_body["message"] = "Email is required"
        return response_body, 400
    if "name" not in data:
        response_body["message"] = "Name is required"
        return response_body, 400    
    if "password" not in data:
        response_body["message"] = "Password is required"
        return response_body, 400
    if "rol" not in data:
        response_body["message"] = "Rol is required"
        return response_body, 400
    # Verificar si el email ya existe.
    user = Users.query.filter_by(email=data['email']).first()    
    if user:
        response_body['message'] = "The email already exist"
        return response_body, 400
    if data['rol'] != 'Admin' and data['rol'] != 'Cocinero' and data['rol'] != 'Jefe de Compras':
        response_body['message'] = "Rol is invalid"
        return response_body, 400     
    # Crear un nuevo usuario
    new_user = Users(email = data['email'],
                     name = data['name'], 
                     rol = data['rol'],
                     password = data['password'],
                     is_active = True)
    db.session.add(new_user)    
    db.session.commit()
    # Crear un token de acceso para el nuevo usuario
    access_token = create_access_token(identity = {'user_id': new_user.id, 'rol': new_user.rol})
    response_body['message'] = "User resgistered succesfull"
    response_body['token'] = access_token
    response_body['user'] = user.serialize()
    return response_body, 201


# ENDPOINT para consultar o dar de alta una linea de albaran GET o POST
@api.route("/delivery_note_lines/<int:delivery_note>", methods=['GET', 'POST'])
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


@api.route('/centers', methods=['GET', 'POST'])
def handle_centers():
    response_body = {}
    results = []
    if request.method == 'GET':
        centers = db.session.query(Centers).scalars()
        response_body['results'] = [row.serialize()for row in centers]
        response_body['message'] = 'GET centers'
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        line = Centers (name = data['name'],
                        address = data['address'], 
                        manager = data['manager'],
                        phone = data['phone'],)                
        db.session.add(line)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = 'POST Method Centers'
        return response_body, 200  
        
          
@api.route('/centers/<int:center_id>', methods=['PUT', 'DELETE'])  
def modify_center(center_id):  
    response_body = {}
    results = []
    if request.method == 'DELETE':
        line = center_id.query.filter_by(center_id = center_id).first()
        if line:
            db.session.delete(line)
            db.session.commit()
            response_body['message'] = f'Center {center_id} has been deleted.'
            return response_body, 200
        else:
            response_body['message'] = f'Could not delete {center_id}.'
            return response_body, 401
    if request.method == 'PUT':
        line = center_id.query.filter_by(center_id = center_id).first()
        if not line:
            response_body['message'] = f'Not found {center_id}'
            return response_body, 404
        data = request.json
        line = Centers (name = data['name'],
                        address = data['address'], 
                        manager = data['manager'],
                        phone = data['phone'],)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = f'Center {center_id} it´s OK!'
        return response_body, 200


@api.route('/delivery_notes', methods=['GET', 'POST'])
def handle_delivery_notes():
    response_body = {}
    results = []
    if request.method == 'GET':
        delivery_notes = db.session.query(DeliveryNotes).scalars()
        response_body['results'] = [row.serialize()for row in delivery_notes]
        response_body['message'] = 'GET delivery_notes'
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        line =  DeliveryNotes (date = data['date'],
                               center_id = data ['center_id'],
                               sum_costs = data ['sum_costs'],
                               sum_totals = data ['sum_totals'],
                               sum_vat = data['sum_vat'],
                               status = data ['status'],
                               user_id = data ['user_id'],)                             
        db.session.add(line)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = 'POST Method DeliveryNotes'
        return response_body, 200  


@api.route('/delivery_note/<int:delivery_note_id>', methods=['PUT', 'DELETE'])  
def modify_delivery_note(delivery_note_id):  
    response_body = {}
    results = []
    if request.method == 'DELETE':
        line = delivery_note_id.query.filter_by(delivery_note_id = delivery_note_id).first()
        if line:
            db.session.delete(line)
            db.session.commit()
            response_body['message'] = f'Delivery Note {delivery_note_id} has been deleted.'
            return response_body, 200
        else:
            response_body['message'] = f'Could not delete {delivery_note_id}.'
            return response_body, 401
    if request.method == 'PUT':
        line = delivery_note_id.query.filter_by(delivery_note_id = delivery_note_id).first()
        if not line:
            response_body['message'] = f'Not found {delivery_note_id}'
            return response_body, 404
        data = request.json
        line =  DeliveryNotes (date = data['date'],
                               center_id = data ['center_id'],
                               sum_costs = data ['sum_costs'],
                               sum_totals = data ['sum_totals'],
                               sum_vat = data['sum_vat'],
                               status = data ['status'],
                               user_id = data ['user_id'],)          
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = f'Delivery Note {delivery_note_id} it´s OK!'
        return response_body, 200








if __name__ == '__main__':
    app.run(debug=True)
#








