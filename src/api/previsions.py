from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, Previsions, Prevision_Lines, ManufacturingOrders
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


api = Blueprint('api', __name__)
CORS(api)  # Allow CORS requests to this API


# ENDPOINT para ver todos los registros de PREVISIONS y crear un GET o POST
@api.route("/previsions", methods['GET','POST'])
@jwt_required()
def handle_previsions():
    response_body = {}
    results = []
    current_user = get_jwt_identity()
    user_id = current_user['user_id']
    if request.method == 'GET':
        # Obtener user_id de los encabezados de la solicitud
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        plan = db.session.execute(db.select(Previsions).where(Prevision.user_id == user_id)).scalars()
        response_body['results'] = [row.serialize() for row in plan]
        response_body['message'] = 'GET Method Previsions'
        return response_body, 200
    
    if request.method == 'POST':
        # Obtener user_id de los encabezados de la solicitud
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        data = request.json
        plan = Previsions ( center_id = data['center_id'],
                            date = data['date'],
                            user_id = user_id,) # este campo no estoy seguro ya que lo tiene que coger del local storage
        db.session.add(plan)
        db.session.commit()
        response_body['results'] = plan.serialize()
        response_body['message'] = 'POST Method Previsions'
        return response_body, 200       


# ENDPOINT para editar o borrar una PREVISIONS PUT o DELETE
@api.route("/prevision/<int:prevision_id>", methods['PUT', 'DELETE'])
def modify_prevision(user_id, prevision_id):
    response_body = {}
    results = []

    if request.method == 'DELETE': # Se puede borrar una preciosion? si pero cuando se hayan borrado tambien todas las prevision_lines
        # Verificar si hay entradas asociadas en Prevision_lines
        prevision_lines_count = Prevision_lines.query.filter_by(prevision_id=prevision_id).count()
        if prevision_lines_count > 0:
            response_body['message'] = f'No se puede borrar la Prevision {prevision_id} mientras tenga entradas en Prevision_lines'
            return response_body, 400
        # Si no hay entradas asociadas, se puede eliminar la Prevision
        # Obtener user_id de los encabezados de la solicitud
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        plan = prevision_id.query.filter_by(user_id = user_id, prevision_id = prevision_id).first()
        if plan:
            db.session.delete(plan)
            db.session.commit()
            response_body['message'] = f'Prevision {prevision_id} del usuario {user_id} ha sido eliminada'
            return response_body, 200            
        else:
            response_body['message'] = f'No se ha podido borrar la prevision {prevision_id}'
            return response_body, 401

    if request.method == 'PUT':
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        plan = prevision_id.query.filter_by(user_id = user_id, prevision_id = prevision_id).first()
        if not plan:
            response_body['message'] = f'No se ha encontrado la prevision {prevision_id}'
            return response_body, 404
        data = request.json
        plan = Prevision (  center_id = data['center_id'],
                            date = data['date'],
                            user_id = user_id,) # este campo lo tiene que coger del local storage
        db.session.commit()
        response_body['results'] = plan.serialize()
        response_body['message'] = f'Prevision {prevision_id} se ha actualizado con exito'
        return response_body, 200       


# ENDPOINT para ver todos los registros de PREVISIONS_LINES y crear un GET o POST
@api.route("/prevision_lines", methods['GET','POST'])
def handle_prevision_lines(user_id):
    response_body = {}
    results = []

    if request.method == 'GET':
        # Obtener user_id de los encabezados de la solicitud
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        planLine = db.session.execute(db.select(Prevision_Lines).where(Prevision_Lines.user_id == user_id)).scalars()
        response_body['results'] = [row.serialize() for row in planLine]
        response_body['message'] = 'GET Method Prevision_Lines'
        return response_body, 200
    
    if request.method == 'POST':
        # Obtener user_id de los encabezados de la solicitud
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        data = request.json
        planLine = PrevisionLines ( prevision_id = data['prevision_id'],
                                    service = data['service'],
                                    pax_service = data['pax_service']
                                    composition_id = data['composition_id'],
                                    user_id = user_id,) # este campo lo tiene que coger del local storage
        db.session.add(planLine)    
        db.session.commit()
        response_body['results'] = planLine.serialize()
        response_body['message'] = 'POST Method Prevision_Line'
        return response_body, 200       


# ENDPOINT para editar o borrar una PREVISIONS_LINES PUT o DELETE
@api.route("/prevision_line/<int:prevision_lines_id>", methods['PUT', 'DELETE'])
def modify_prevision(user_id, prevision_lines_id):
    response_body = {}
    results = []

    if request.method == 'DELETE':
        # Obtener user_id de los encabezados de la solicitud
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        planLine = prevision_lines_id.query.filter_by(user_id = user_id, prevision_lines_id = prevision_lines_id).first()
        if planLine:
            db.session.delete(planLine)
            db.session.commit()
            response_body['message'] = f'Prevision Line {prevision_lines_id} del usuario {user_id} ha sido eliminada'
            return response_body, 200            
        else:
            response_body['message'] = f'No se ha podido borrar la Linea de Prevision {prevision_lines_id}'
            return response_body, 401

    if request.method == 'PUT':
        # Obtener user_id de los encabezados de la solicitud
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        planLine = prevision_lines_id.query.filter_by(user_id = user_id, prevision_lines_id = prevision_lines_id).first()
        if not planLine:
            response_body['message'] = f'No se ha encontrado la prevision line {prevision_lines_id}'
            return response_body, 404
        data = request.json
        planLine = PrevisionLines ( prevision_id = data['prevision_id'],
                                    service = data['service'],
                                    pax_service = data['pax_service'],
                                    composition_id = data['composition_id'],) # este campo lo tiene que coger del local storage
        db.session.commit()
        response_body['results'] = planLine.serialize()
        response_body['message'] = f'Prevision Line {prevision_lines_id} se ha actualizado con exito'
        return response_body, 200     


# ENDPOINT para leer o crear MANUFACTURING_ORDERS GET or POST
@api.route("/manufacturing_ord", methods['GET','POST'])
def handle_manufacturing(user_id):
    response_body = {}
    results = []

    if request.method == 'GET':
        # Obtener user_id de los encabezados de la solicitud
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        data = db.session.execute(db.select(ManufacturingOrders).where(ManufacturingOrders.user_id == user_id)).scalars()
        response_body['results'] = [row.serialize() for row in data]
        response_body['message'] = 'GET Method Prevision_Lines'
        return response_body, 200
    
    if request.method == 'POST':
        # Obtener user_id de los encabezados de la solicitud
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        data = request.json
        plan = ManufacturingOrders (recipe_id = data['recipe_id'],
                                    delivery_date = data['delivery_date'],
                                    qty = data['qty']
                                    status = data['status'],
                                    user_id = user_id,) # este campo lo tiene que coger del local storage
        db.session.add(plan)    
        db.session.commit()
        response_body['results'] = plan.serialize()
        response_body['message'] = 'POST Method Prevision_Line'
        return response_body, 200 


# ENDPOINT para borrar o actualizar MANUFACTURING_ORDERS DELETE or PUT
@api.route("/manufacturing_ord/<int:manufacturing_orders_id>", methods['PUT', 'DELETE'])
def modify_manufacturing(user_id, manufacturing_orders_id):
    response_body = {}
    results = []

    if request.method == 'DELETE':
        # Obtener user_id de los encabezados de la solicitud
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        plan = manufacturing_orders_id.query.filter_by(user_id = user_id, manufacturing_orders_id = manufacturing_orders_id).first()
        if plan:
            db.session.delete(plan)
            db.session.commit()
            response_body['message'] = f'Manufacturing Order {manufacturing_orders_id} del usuario {user_id} ha sido eliminada'
            return response_body, 200            
        else:
            response_body['message'] = f'No se ha podido borrar la manufacturing order {manufacturing_orders_id}'
            return response_body, 401

    if request.method == 'PUT':
        # Obtener user_id de los encabezados de la solicitud
        user_id = request.headers.get('user_id') # Almacenar en el Local Storage el user_id
        if user_id is None:
            response_body['message'] = 'user_id no proporcionado en los encabezados de la solicitud'
            return response_body, 400
        plan = manufacturing_orders_id.query.filter_by(user_id = user_id, manufacturing_orders_id = manufacturing_orders_id).first()
        if not plan:
            response_body['message'] = f'No se ha encontrado la manufacturing order {manufacturing_orders_id}'
            return response_body, 404
        data = request.json
        plan = ManufacturingOrders (recipe_id = data['recipe_id'],
                                    delivery_date = data['delivery_date'],
                                    qty = data['qty']
                                    status = data['status'],
                                    user_id = user_id,) # este campo lo tiene que coger del local storage
        db.session.commit()
        response_body['results'] = plan.serialize()
        response_body['message'] = f'Manufacturing order {manufacturing_orders_id} se ha actualizado con exito'
        return response_body, 200  