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
    new_user = Users   (email = data['email'],
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
        line =  DeliveryNotes  (date = data['date'],
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
        line =  DeliveryNotes  (date = data['date'],
                                center_id = data ['center_id'],
                                sum_costs = data ['sum_costs'],
                                sum_totals = data ['sum_totals'],
                                sum_vat = data['sum_vat'],
                                status = data ['status'],
                                user_id = data ['user_id'],)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = f'Delivery Note {delivery_note_id} it is OK!'
        return response_body, 200


@api.route("/delivery_note_lines/<int:delivery_note_id>", methods=['GET', 'POST'])
def handle_delivery_lines(delivery_note_id):
    response_body = {}
    results = []
    if request.method == 'GET':
        line = DeliveryNoteLines.query.filter_by(delivery_note_line_id = delivery_note_line_id).scalars()
        response_body['results'] = [row.serialize() for row in line]
        response_body['message'] = 'GET Method Delivery Note Line'
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        line = DeliveryNoteLines   (qty = data['qty'],
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


@api.route("/delivery_note_lines/<int:user_id>/delivery_line/<int:delivery_note_line_id>", methods=['DELETE', 'PUT'])
@jwt_required()
def modify_delivery_lines(delivery_note_lines_id):
    response_body = {}
    results = []
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
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
        line = DeliveryNoteLines.query.filter_by(user_id = user_id, delivery_note_lines_id = delivery_note_lines_id).first()
        if not line:
            response_body['message'] = f'No se ha encontrado la linea {delivery_note_line_id}'
            return response_body, 404
        data = request.json
        line = DeliveryNoteLines   (qty = data['qty'],
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
        line = Centers.query.filter_by(center_id = center_id).first()
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
        response_body['message'] = f'Center {center_id} it is OK!'
        return response_body, 200


@api.route('/compositions', methods=['GET', 'POST'])
def handle_compositions():
    response_body = {}
    results = []
    if request.method == 'GET':
        compositions = db.session.query(Compositions).scalars()
        response_body['results'] = [row.serialize()for row in compositions]
        response_body['message'] = 'GET compositions'
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        line = Compositions(name = data['name'],
                            cost = data['cost'],)
        db.session.add(line)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = 'POST Method Compositions'
        return response_body, 200


@api.route('/compositions/<int:compositions_id>', methods=['PUT', 'DELETE'])
def modify_compositions(compositions_id):
    response_body = {}
    results = []
    if request.method == 'DELETE':
        line = Compositions.query.filter_by(compositions_id = compositions_id).first()
        if line:
            db.session.delete(line)
            db.session.commit()
            response_body['message'] = f'Composition {compositions_id} has been deleted.'
            return response_body, 200
        else:
            response_body['message'] = f'Could not delete {compositions_id}.'
            return response_body, 401
    if request.method == 'PUT':
        line = Compositions.query.filter_by(compositions_id = compositions_id).first()
        if not line:
            response_body['message'] = f'Not found {compositions_id}'
            return response_body, 404
        data = request.json
        line = Compositions(name = data['name'],
                            cost = data['cost'],)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = f'Compositions {compositions_id} it is OK!'
        return response_body, 200


@api.route('/composition_lines', methods=['GET', 'POST'])
def handle_compositions_Line():
    response_body = {}
    results = []
    if request.method == 'GET':
        compositions = db.session.query(CompositionLines).scalars()
        response_body['results'] = [row.serialize()for row in compositions]
        response_body['message'] = 'GET Composition Line'
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        line = Compositions(recipe_id = data['recipe_id'],
                            units_recipe = data['units_recipe'],
                            cost_unit_line = data['cost_unit_line'],
                            composition_id = data['composition_id'],)
        db.session.add(line)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = 'POST Method Composition Line'
        return response_body, 200


@api.route('/composition_Lines/<int:composition_line_id>', methods=['PUT', 'DELETE'])
def modify_composition_line(compositions_line_id):
    response_body = {}
    results = []
    if request.method == 'DELETE':
        line = CompositionLines.query.filter_by(composition_line_id = composition_line_id).first()
        if line:
            db.session.delete(line)
            db.session.commit()
            response_body['message'] = f'Composition Line {composition_line_id} has been deleted.'
            return response_body, 200
        else:
            response_body['message'] = f'Could not delete {composition_line_id}.'
            return response_body, 401
    if request.method == 'PUT':
        line = CompositionLines.query.filter_by(composition_line_id = composition_line_id).first()
        if not line:
            response_body['message'] = f'Not found {composition_line_id}'
            return response_body, 404
        data = request.json
        line = CompositionLines(recipe_id = data['recipe_id'],
                                units_recipe = data['units_recipe'],
                                cost_unit_line = data['cost_unit_line'],
                                composition_id = data['composition_id'],)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = f'Compositions Line {composition_line_id} it is OK!'
        return response_body, 200


@api.route('/recipes', methods=['GET', 'POST'])
def handle_recipes():
    response_body = {}
    results = []
    if request.method == 'GET':
        recipes = db.session.query(Recipes).scalars()
        response_body['results'] = [row.serialize()for row in recipes]
        response_body['message'] = 'GET Recipes'
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        line = Recipes (name = data['name'],
                        is_active = data['is_active'],
                        meals = data ['meals'],
                        cost_meals = data ['cost_meals'],)
        db.session.add(line)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = 'POST Method Recipes'
        return response_body, 200


@api.route('/recipes/<int:recipes_id>', methods=['PUT', 'DELETE'])
def modify_recipes(recipes_id):
    response_body = {}
    results = []
    if request.method == 'DELETE':
        line = Recipes.query.filter_by(recipes_id = recipes_id).first()
        if line:
            db.session.delete(line)
            db.session.commit()
            response_body['message'] = f'Recipe {recipes_id} has been deleted.'
            return response_body, 200
        else:
            response_body['message'] = f'Could not delete {recipes_id}.'
            return response_body, 401
    if request.method == 'PUT':
        line = Recipes.query.filter_by(recipes_id = recipes_id).first()
        if not line:
            response_body['message'] = f'Not found {recipes_id}'
            return response_body, 404
        data = request.json
        line = Recipes (name = data['name'],
                        is_active = data['is_active'],
                        meals = data ['meals'],
                        cost_meals = data ['cost_meals'],)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = f'Recipes {recipes_id} it is OK!'
        return response_body, 200


@api.route('/line_recipes', methods=['GET', 'POST'])
def handle_line_recipe():
    response_body = {}
    results = []
    if request.method == 'GET':
        line_recipes = db.session.query(LineRecipes).scalars()
        response_body['results'] = [row.serialize()for row in line_recipe]
        response_body['message'] = 'GET line recipe'
        return response_body, 200
    if request.method == 'POST':
        data = request.json
        line = LineRecipes (recipe_id = data['recipe_id'],
                            reference_id = data['reference_id'],
                            qty = data ['qty'],
                            cost = data ['cost'],
                            total = data ['total'],
                            units = data ['units'],
                            cost_unit = data ['cost_unit'],)
        db.session.add(line)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = 'POST Method Line Recipe'
        return response_body, 200


@api.route('/line_recipes/<int:line_recipes_id>', methods=['PUT', 'DELETE'])
def modify_line_recipes(line_recipes_id):
    response_body = {}
    results = []
    if request.method == 'DELETE':
        line = LineRecipes.query.filter_by(line_recipes_id = line_recipes_id).first()
        if line:
            db.session.delete(line)
            db.session.commit()
            response_body['message'] = f'Line recipe {line_recipes_id} has been deleted.'
            return response_body, 200
        else:
            response_body['message'] = f'Could not delete {line_recipes_id}.'
            return response_body, 401
    if request.method == 'PUT':
        line = LineRecipes.query.filter_by(line_recipes_id = line_recipes_id).first()
        if not line:
            response_body['message'] = f'Not found {line_recipes_id}'
            return response_body, 404
        data = request.json
        line = LineRecipes (recipe_id = data['recipe_id'],
                            reference_id = data['reference_id'],
                            qty = data ['qty'],
                            cost = data ['cost'],
                            total = data ['total'],
                            units = data ['units'],
                            cost_unit = data ['cost_unit'],)
        db.session.commit()
        response_body['results'] = line.serialize()
        response_body['message'] = f'Line recipes {line_recipes_id} it is OK!'
        return response_body, 200


@api.route("/previsions", methods['GET','POST'])
@jwt_required()
def handle_previsions():
    response_body = {}
    results = []
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    if request.method == 'GET':
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        plan = db.session.execute(db.select(Previsions).where(Prevision.user_id == user_id)).scalars()
        response_body['results'] = [row.serialize() for row in plan]
        response_body['message'] = 'GET Method Previsions'
        return response_body, 200
    if request.method == 'POST':
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        data = request.json
        plan = Previsions  (center_id = data['center_id'],
                            date = data['date'],
                            user_id = user_id,)
        db.session.add(plan)
        db.session.commit()
        response_body['results'] = plan.serialize()
        response_body['message'] = 'POST Method Previsions'
        return response_body, 200


@api.route("/prevision/<int:prevision_id>", methods['PUT', 'DELETE'])
@jwt_required()
def modify_prevision(prevision_id):
    response_body = {}
    results = []
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    if request.method == 'DELETE':
        # Verificar si hay entradas asociadas en Prevision_lines
        prevision_lines_count = Prevision_lines.query.filter_by(prevision_id=prevision_id).count()
        if prevision_lines_count > 0:
            response_body['message'] = f'No se puede borrar la Prevision {prevision_id} mientras tenga entradas en Prevision_lines'
            return response_body, 400
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        plan = Previsions.query.filter_by(user_id = user_id, prevision_id = prevision_id).first()
        if plan:
            db.session.delete(plan)
            db.session.commit()
            response_body['message'] = f'Prevision {prevision_id} del usuario {user_id} ha sido eliminada'
            return response_body, 200
        else:
            response_body['message'] = f'No se ha podido borrar la prevision {prevision_id}'
            return response_body, 401
    if request.method == 'PUT':# Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        plan = Previsions.query.filter_by(user_id = user_id, prevision_id = prevision_id).first()
        if not plan:
            response_body['message'] = f'No se ha encontrado la prevision {prevision_id}'
            return response_body, 404
        data = request.json
        plan = Prevision   (center_id = data['center_id'],
                            date = data['date'],
                            user_id = user_id,)
        db.session.commit()
        response_body['results'] = plan.serialize()
        response_body['message'] = f'Prevision {prevision_id} se ha actualizado con exito'
        return response_body, 200


@api.route("/prevision_lines", methods['GET','POST'])
@jwt_required()
def handle_prevision_lines():
    response_body = {}
    results = []
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    if request.method == 'GET':
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        planLine = db.session.execute(db.select(Prevision_Lines).where(Prevision_Lines.user_id == user_id)).scalars()
        response_body['results'] = [row.serialize() for row in planLine]
        response_body['message'] = 'GET Method Prevision_Lines'
        return response_body, 200
    if request.method == 'POST':
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        data = request.json
        planLine = PrevisionLines ( prevision_id = data['prevision_id'], #este campo lo tiene que heredar
                                    service = data['service'],
                                    pax_service = data['pax_service'],
                                    composition_id = data['composition_id'],
                                    user_id = user_id,)
        db.session.add(planLine)
        db.session.commit()
        response_body['results'] = planLine.serialize()
        response_body['message'] = 'POST Method Prevision_Line'
        return response_body, 200


@api.route("/prevision_line/<int:prevision_lines_id>", methods['PUT', 'DELETE'])
@jwt_required()
def modify_prevision(prevision_lines_id):
    response_body = {}
    results = []
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    if request.method == 'DELETE':
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        planLine = PrevisionLines.query.filter_by(user_id = user_id, prevision_lines_id = prevision_lines_id).first()
        if planLine:
            db.session.delete(planLine)
            db.session.commit()
            response_body['message'] = f'Prevision Line {prevision_lines_id} del usuario {user_id} ha sido eliminada'
            return response_body, 200
        else:
            response_body['message'] = f'No se ha podido borrar la Linea de Prevision {prevision_lines_id}'
            return response_body, 401
    if request.method == 'PUT':
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        planLine = PrevisionLines.query.filter_by(user_id = user_id, prevision_lines_id = prevision_lines_id).first()
        if not planLine:
            response_body['message'] = f'No se ha encontrado la prevision line {prevision_lines_id}'
            return response_body, 404
        data = request.json
        planLine = PrevisionLines ( prevision_id = data['prevision_id'],
                                    service = data['service'],
                                    pax_service = data['pax_service'],
                                    composition_id = data['composition_id'],)
        db.session.commit()
        response_body['results'] = planLine.serialize()
        response_body['message'] = f'Prevision Line {prevision_lines_id} se ha actualizado con exito'
        return response_body, 200


@api.route("/manufacturing_ord", methods['GET','POST'])
@jwt_required()
def handle_manufacturing():
    response_body = {}
    results = []
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    if request.method == 'GET':
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        data = db.session.execute(db.select(ManufacturingOrders).where(ManufacturingOrders.user_id == user_id)).scalars()
        response_body['results'] = [row.serialize() for row in data]
        response_body['message'] = 'GET Method Prevision_Lines'
        return response_body, 200
    if request.method == 'POST':
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        data = request.json
        plan = ManufacturingOrders (recipe_id = data['recipe_id'],
                                    delivery_date = data['delivery_date'],
                                    qty = data['qty'],
                                    status = data['status'],
                                    user_id = user_id,) #
        db.session.add(plan)
        db.session.commit()
        response_body['results'] = plan.serialize()
        response_body['message'] = 'POST Method Prevision_Line'
        return response_body, 200


@api.route("/manufacturing_ord/<int:manufacturing_orders_id>", methods['PUT', 'DELETE'])
@jwt_required()
def modify_manufacturing(manufacturing_orders_id):
    response_body = {}
    results = []
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    if request.method == 'DELETE':
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        plan = ManufacturingOrders.query.filter_by(user_id = user_id, manufacturing_orders_id = manufacturing_orders_id).first()
        if plan:
            db.session.delete(plan)
            db.session.commit()
            response_body['message'] = f'Manufacturing Order {manufacturing_orders_id} del usuario {user_id} ha sido eliminada'
            return response_body, 200
        else:
            response_body['message'] = f'No se ha podido borrar la manufacturing order {manufacturing_orders_id}'
            return response_body, 401
    if request.method == 'PUT':
        if user_id is None:
            response_body['message'] = 'Usuario no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        plan = manufacturing_orders_id.query.filter_by(user_id = user_id, manufacturing_orders_id = manufacturing_orders_id).first()
        if not plan:
            response_body['message'] = f'No se ha encontrado la manufacturing order {manufacturing_orders_id}'
            return response_body, 404
        data = request.json
        plan = ManufacturingOrders (recipe_id = data['recipe_id'],
                                    delivery_date = data['delivery_date'],
                                    qty = data['qty'],
                                    status = data['status'],
                                    user_id = user_id,)
        db.session.commit()
        response_body['results'] = plan.serialize()
        response_body['message'] = f'Manufacturing order {manufacturing_orders_id} se ha actualizado con exito'
        return response_body, 200



if __name__ == '__main__':
    app.run(debug=True)









