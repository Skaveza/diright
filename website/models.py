from . import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'doctor' or 'admin'

class PatientDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(150), nullable=False)
    document = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.Text, nullable=True)
