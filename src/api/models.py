from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    rol = db.Column(db.Enum('Admin', 'Jefe de Compras', 'Cocinero', name="rol"), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User: {self.id} - {self.email}>'

    def serialize(self):
        return {'id': self.id,
                'email': self.email,
                'rol': self.rol,
                'is_active': self.is_active}


class Centers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    manager = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.Integer)

    def __repr__(self):
        return f'<Center: {self.id} - {self.name}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'address': self.address,
                'manager': self.manager,
                'phone': self.phone}


class Compositions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Composition: {self.id} - {self.name}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'cost': self.cost}


class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    meals = db.Column(db.Integer, nullable=False)
    cost_meals = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Recipe: {self.id} - {self.name}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'is_active': self.is_active,
                'meals': self.meals,
                'cost_meals': self.cost_meals}


class Supliers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.Integer)  
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Suplier: {self.id} - {self.name}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'phone': self.phone,
                'email': self.email}


class References(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    category = db.Column(db.Enum('Alimento Fresco', 'Alimento Congelado', 'Conserva', 'Bebida', 'Licor', name="category"), nullable=False)
    units = db.Column(db.Enum('ud', 'gr', 'ml', 'kg', 'l', name="units"), nullable=False)
    id_suplier = db.Column(db.Integer, db.ForeignKey('supliers.id'))
    cost = db.Column(db.Integer, nullable=False)
    vat = db.Column(db.Enum('4', '10', '21', name="vat"), nullable=False)
    purchase_format = db.Column(db.Integer)

    def __repr__(self):
        return f'<Reference: {self.id} - {self.name}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'category': self.category,
                'units': self.units,
                'id_suplier': self.id_suplier,
                'cost': self.cost,
                'vat': self.vat,
                'purchase_format': self.purchase_format}


class Previsions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    service = db.Column(db.Enum('Desayuno', 'Almuerzo', 'Cena', name="service"), nullable=False)
    pax_service = db.Column(db.Integer, nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey('centers.id'))
    composition_id = db.Column(db.Integer, db.ForeignKey('compositions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    center_to = db.relationship('Centers', foreign_keys=[center_id])
    composition_to = db.relationship('Compositions', foreign_keys=[composition_id])   
    user_to = db.relationship('Users', foreign_keys=[user_id])

    def __repr__(self):
        return f'<Prevision: {self.id} - Center: {self.center_id}>'

    def serialize(self):
        return {'id': self.id,
                'center_id': self.center_id,
                'date': self.date,
                'service': self.service,
                'pax_service': self.pax_service,
                'composition_id': self.composition_id,
                'user_id': self.user_id}


class DeliveryNotes(db.Model):
    __tablename__ = "delivery_notes"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    sum_costs = db.Column(db.Integer, nullable=False)
    sum_totals = db.Column(db.Integer, nullable=False)
    sum_vat = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('Hoja de Envio', 'Albaran', name="status"), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    center_id = db.Column(db.Integer, db.ForeignKey('centers.id'))
    center = db.relationship('Centers', foreign_keys=[center_id])
    user = db.relationship('Users', foreign_keys=[user_id])

    def __repr__(self):
        return f'<Delivery Notes: {self.id} - Center: {self.center_id}>'

    def serialize(self):
        return {'id': self.id,
                'date': self.date,
                'center_id': self.center_id,
                'sum_costs': self.sum_costs,
                'sum_totals': self.sum_totals,
                'sum_vat': self.sum_vat,
                'status': self.status,
                'user_id': self.user_id}


class DeliveryNoteLines(db.Model):
    __tablename__ = "delivery_note_lines"
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    unit_cost = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    vat = db.Column(db.Enum('4', '10', '21', name="vat"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    delivery_note_id = db.Column(db.Integer, db.ForeignKey('delivery_notes.id'))
    recipe_to = db.relationship('Recipes', foreign_keys=[recipe_id])
    delivery_to = db.relationship('DeliveryNotes', foreign_keys=[delivery_note_id])

    def __repr__(self):
        return f'<Delivery Note Line: {self.id} - {self.recipe_id} - {self.delivery_note_id}>'

    def serialize(self):
        return {'id': self.id,
                'recipe_id': self.recipe_id,
                'delivery_note_id': self.delivery_note_id,
                'qty': self.qty,
                'cost': self.cost,
                'total': self.total,
                'vat': self.vat}


class CompositionLines(db.Model):
    __tablename__ = "composition_lines"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    units_recipe = db.Column(db.Integer, nullable=False)
    cost_unit_line = db.Column(db.Integer, nullable=False)
    composition_id = db.Column(db.Integer, db.ForeignKey('compositions.id'))
    recipe_to = db.relationship('Recipes', foreign_keys=[recipe_id])
    composition_to = db.relationship('Compositions', foreign_keys=[composition_id])  

    def __repr__(self):
        return f'<CompositionLine: {self.id} - {self.recipe_id}>'

    def serialize(self):
        return {'id': self.id,
                'recipe_id': self.recipe_id,
                'units_recipe': self.units_recipe,
                'cost_unit_line': self.cost_unit_line,
                'composition_id': self.composition_id}


class LineRecipes(db.Model):
    __tablename__ = "line_recipes"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('references.id'))
    qty = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    units = db.Column(db.Integer, nullable=False)
    cost_unit = db.Column(db.Integer, nullable=False)
    reference_to = db.relationship('References', foreign_keys=[reference_id])
    recipe_to = db.relationship('Recipes', foreign_keys=[recipe_id])

    def __repr__(self):
        return f'<Line Recipe: {self.id} - {self.recipe_id} - {self.reference_id}>'

    def serialize(self):
        return {'id': self.id,
                'recipe_id': self.recipe_id,
                'reference_id': self.reference_id,
                'qty': self.qty,
                'cost': self.cost,
                'total': self.total,
                'units': self.units,
                'cost_unit': self.cost_unit}


class ManufacturingOrders(db.Model):
    __tablename__ = "manufacturing_orders"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    delivery_date = db.Column(db.DateTime, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('Pendiente', 'En Proceso', 'Fabricado', 'Almacenado', 'Enviado', name="status"), nullable=False)
    recipe_to = db.relationship('Recipes', foreign_keys=[recipe_id])
    

    def __repr__(self):
        return f'<Composition Line: {self.id} - Recipe: {self.recipe_id}>'

    def serialize(self):
        return {'id': self.id,
                'recipe_id': self.recipe_id,
                'delivery_date': self.delivery_date,
                'qty': self.qty,
                'status': self.status}