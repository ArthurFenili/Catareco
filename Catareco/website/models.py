from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    balance = db.Column(db.Integer)
    all_time_PET = db.Column(db.Integer)
    all_time_ALUMINUM = db.Column(db.Integer)
