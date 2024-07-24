import random
import string

def generate_patient_id():
    # Generate a random 8-character alphanumeric ID
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for i in range(8))

def create_new_patient():
    patient_id = generate_patient_id()
    # Here you would typically also create a new patient record in your database
    # For example:
    # new_patient = Patient(patient_id=patient_id)
    # db.session.add(new_patient)
    # db.session.commit()
    return patient_id