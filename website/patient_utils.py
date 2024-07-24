from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(8), unique=True, nullable=False)

def generate_patient_id():
    # Generate a random 8-character alphanumeric ID
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

def create_new_patient():
    patient_id = generate_patient_id()
    
    new_patient = Patient(patient_id=patient_id)
    db.session.add(new_patient)
    db.session.commit()
    return patient_id

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database and tables created.")
        
        new_patient_id = create_new_patient()
        print(f"New patient created with ID: {new_patient_id}")
