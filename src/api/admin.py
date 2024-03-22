import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from api.models import db, Users, Centers, Compositions, Recipes, Suppliers, References, Previsions, DeliveryNotes, DeliveryNoteLines, CompositionLines, LineRecipes, ManufacturingOrders

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(ModelView(Users, db.session))  # You can duplicate that line to add mew models
    admin.add_view(ModelView(Centers, db.session))
    admin.add_view(ModelView(Compositions, db.session))
    admin.add_view(ModelView(Recipes, db.session))
    admin.add_view(ModelView(Suppliers, db.session))
    admin.add_view(ModelView(References, db.session))
    admin.add_view(ModelView(Previsions, db.session))
    admin.add_view(ModelView(DeliveryNotes, db.session))
    admin.add_view(ModelView(DeliveryNoteLines, db.session))
    admin.add_view(ModelView(CompositionLines, db.session))
    admin.add_view(ModelView(LineRecipes, db.session))
    admin.add_view(ModelView(ManufacturingOrders, db.session))
