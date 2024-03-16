from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    rol = db.Column(db.Enum('Admin', 'Jefe de Compras', 'Cocinero', name="Rol"), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<Users: {self.id} - {self.email} - {self.rol} - {self.is_active}>'

    def serialize(self):
        # Do not serialize the password, its a security breach
        return {'id': self.id,
                'email': self.email,
                'rol': self.rol,
                'is_active': self.is_active}


class Center(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    manager = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.Integer)

    def __repr__(self):
        return f'<Center: {self.id} - {self.name} - {self.address} - {self.manager} - {self.phone}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'address': self.address,
                'manager': self.manager,
                'phone': self.phone}


class Composition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    sum_costs = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Composition: {self.id} - {self.name} - {self.sum_costs}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'sum_costs': self.sum_costs}


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    units = db.Column(db.Integer, nullable=False)
    cost_unit = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Recipe: {self.id} - {self.name} - {self.is_active} - {self.units} - {self.cost_unit}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'is_active': self.is_active,
                'units': self.units,
                'cost_unit': self.cost_unit}


class Suplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.Integer)  
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Suplier: {self.id} - {self.name} - {self.phone} - {self.email}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'phone': self.phone,
                'email': self.email}


class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    category = db.Column(db.Enum('Alimento Fresco', 'Alimento Congelado', 'Conserva', 'Bebida', 'Licor', name="Category"), nullable=False)
    units = db.Column(db.Enum('ud', 'gr', 'ml', 'kg', 'l'), nullable=False)
    id_suplier = db.Column(db.Integer, db.ForeignKey('suplier.id'))
    cost = db.Column(db.Integer, nullable=False)
    vat = db.Column(db.Enum('4', '10', '21', name="VAT"), nullable=False)
    purchase_format = db.Column(db.Integer)

    def __repr__(self):
        return f'<Reference: {self.id} - {self.name} - {self.category} - {self.units} - {self.id_suplier} - {self.cost} - {self.vat} - {self.purchase_format}>'

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'category': self.category,
                'units': self.units,
                'id_suplier': self.id_suplier,
                'cost': self.cost,
                'vat': self.vat,
                'purchase_format': self.purchase_format}


class Prevision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'))
    date = db.Column(db.DateTime, nullable=False)
    service = db.Column(db.Enum('Desayuno', 'Almuerzo', 'Cena', name="Service"), nullable=False)
    pax_service = db.Column(db.Integer, nullable=False)
    composition_id = db.Column(db.Integer, db.ForeignKey('composition.id'))
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    center_to = db.relationship('Center', foreign_keys=[center_id])
    composition_to = db.relationship('Composition', foreign_keys=[composition_id])   
    user_to = db.relationship('Users', foreign_keys=[users_id])

    def __repr__(self):
        return f'<Prevision: {self.id} - {self.id_centre} - {self.date} - {self.service} - {self.pax_service} - {self.id_composition} - {self.id_user}>'

    def serialize(self):
        return {'id': self.id,
                'id_centre': self.id_centre,
                'date': self.date,
                'service': self.service,
                'pax_service': self.pax_service,
                'id_composition': self.id_composition,
                'id_user': self.id_user}


class DeliveryNotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'))
    sum_costs = db.Column(db.Integer, nullable=False)
    sum_totals = db.Column(db.Integer, nullable=False)
    sum_vat = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('Hoja de Envio', 'Albaran', name="Status"), nullable=False)
    users_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    center = db.relationship('Center', foreign_keys=[center_id])
    user = db.relationship('Users', foreign_keys=[users_id])

    def __repr__(self):
        return f'<DeliveryNotes: {self.id} - {self.date} - {self.id_center} - {self.sum_costs} - {self.sum_totals} - {self.sum_vat} - {self.status} - {self.id_user}>'

    def serialize(self):
        return {'id': self.id,
                'date': self.date,
                'id_center': self.id_center,
                'sum_costs': self.sum_costs,
                'sum_totals': self.sum_totals,
                'sum_vat': self.sum_vat,
                'status': self.status,
                'id_user': self.id_user}


class DeliveryNotesLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe_name = db.Column(db.Integer, db.ForeignKey('recipe.name'))
    delivery_notes_id = db.Column(db.Integer, db.ForeignKey('delivery_notes.id'))
    qty = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    vat = db.Column(db.Enum('4', '10', '21', name="VAT"), nullable=False)
    recipe_to = db.relationship('Recipe', foreign_keys=[recipe_id])
    name_recipe_to = db.relationship('Recipe', foreign_keys=[recipe_name])
    delivery_to = db.relationship('DeliveryNotes', foreign_keys=[delivery_notes_id])

    def __repr__(self):
        return f'<DeliveryNotesLine: {self.id} - {self.id_recipe} - {self.name_recipe} - {self.id_delivery_note} - {self.qty} - {self.cost} - {self.total} - {self.vat}>'

    def serialize(self):
        return {'id': self.id,
                'id_recipe': self.id_recipe,
                'name_recipe': self.name_recipe,
                'id_delivery_note': self.id_delivery_note,
                'qty': self.qty,
                'cost': self.cost,
                'total': self.total,
                'vat': self.vat}


class CompositionLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe_name = db.Column(db.Integer, db.ForeignKey('recipe.name'))
    units_recipe = db.Column(db.Integer, nullable=False)
    cost_unit_line = db.Column(db.Integer, nullable=False)
    composition_id = db.Column(db.Integer, db.ForeignKey('composition.id'))
    recipe_to = db.relationship('Recipe', foreign_keys=[recipe_id])
    name_recipe_to = db.relationship('Recipe', foreign_keys=[recipe_name])
    composition = db.relationship('Composition', foreign_keys=[composition_id])  

    def __repr__(self):
        return f'<CompositionLine: {self.id} - {self.id_recipe} - {self.name_recipe} - {self.units_recipe} - {self.cost_unit_line} - {self.id_composition}>'

    def serialize(self):
        return {'id': self.id,
                'id_recipe': self.id_recipe,
                'name_recipe': self.name_recipe,
                'units_recipe': self.units_recipe,
                'cost_unit_line': self.cost_unit_line,
                'id_composition': self.id_composition}


class LineRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    reference_id = db.Column(db.Integer, db.ForeignKey('reference.id'))
    name_reference = db.Column(db.String(20), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    units = db.Column(db.Integer, nullable=False)
    cost_unit = db.Column(db.Integer, nullable=False)
    reference = db.relationship('Reference', foreign_keys=[reference_id])
    recipe_to = db.relationship('Recipe', foreign_keys=[recipe_id])

    def __repr__(self):
        return f'<LineRecipe: {self.id} - {self.id_recipe} - {self.id_reference} - {self.name_reference} - {self.qty} - {self.cost} - {self.total} - {self.units} - {self.cost_unit}>'

    def serialize(self):
        return {'id': self.id,
                'id_recipe': self.id_recipe,
                'id_reference': self.id_reference,
                'name_reference': self.name_reference,
                'qty': self.qty,
                'cost': self.cost,
                'total': self.total,
                'units': self.units,
                'cost_unit': self.cost_unit}


class ManufacturingOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    recipe_name = db.Column(db.String(50), db.ForeignKey('recipe.name'))
    delivery_date = db.Column(db.DateTime, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('Pendiente', 'En Proceso', 'Fabricado', 'Almacenado', 'Enviado', name="Status"), nullable=False)
    id_recipe_to = db.relationship('Recipe', foreign_keys=[recipe_id])
    name_recipe_to = db.relationship('Recipe', foreign_keys=[recipe_name])

    def __repr__(self):
        return f'<CompositionLine: {self.id} - {self.id_recipe} - {self.name_recipe} - {self.delivery_date} - {self.qty} - {self.status}>'

    def serialize(self):
        return {'id': self.id,
                'id_recipe': self.id_recipe,
                'name_recipe': self.name_recipe,
                'delivery_date': self.delivery_date,
                'qty': self.qty,
                'status': self.status}