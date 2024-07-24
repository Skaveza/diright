from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import PatientDocument, User
from . import db
import pandas as pd
from .patient_utils import create_new_patient
views = Blueprint('views', __name__)

# Load the machine learning model
from .ml_module import predict_diagnosis

@views.route('/')
@login_required
def home():
    if current_user.role == 'doctor':
        return render_template('doctor_home.html', user=current_user)
    elif current_user.role == 'admin':
        return render_template('admin_home.html', user=current_user)
    return render_template('index.html')

@views.route('/new_patient', methods=['GET', 'POST'])
@login_required
def new_patient():
    if current_user.role == 'doctor':
        if request.method == 'POST':
            patient_id = create_new_patient()
            flash(f'New patient created with ID: {patient_id}', 'success')
            return redirect(url_for('views.patient', patient_id=patient_id))
        return render_template('new_patient.html')
    return redirect(url_for('views.home'))

@views.route('/patient/<patient_id>', methods=['GET'])
@login_required
def patient(patient_id):
    if current_user.role == 'doctor':
        document = PatientDocument.query.filter_by(patient_id=patient_id).first()
        if document:
            return render_template('patient_document.html', document=document)
        else:
            flash('No documents found for this patient ID', 'error')
            return redirect(url_for('views.home'))
    return redirect(url_for('views.home'))

@views.route('/update_document', methods=['POST'])
@login_required
def update_document():
    if current_user.role == 'doctor':
        patient_id = request.form.get('patient_id')
        symptoms = request.form.get('symptoms')
        diagnosis = request.form.get('diagnosis')

        document = PatientDocument.query.filter_by(patient_id=patient_id).first()
        if document:
            document.symptoms = symptoms
            document.diagnosis = diagnosis
            db.session.commit()
            flash('Document updated successfully', 'success')
        else:
            flash('No documents found for this patient ID', 'error')
    
    return redirect(url_for('views.home'))

@views.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.role == 'admin':
        users = User.query.all()
        return render_template('manage_users.html', users=users)
    
    return redirect(url_for('views.home'))

@views.route('/update_user', methods=['POST'])
@login_required
def update_user():
    if current_user.role == 'admin':
        user_id = request.form.get('user_id')
        role = request.form.get('role')

        user = User.query.get(user_id)
        if user:
            user.role = role
            db.session.commit()
            flash('User updated successfully', 'success')
        else:
            flash('User not found', 'error')
    
    return redirect(url_for('views.manage_users'))

@views.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if current_user.role == 'doctor':
        if request.method == 'POST':
            symptoms = [
                request.form.get('symptom1'),
                request.form.get('symptom2'),
                request.form.get('symptom3')
            ]
            medical_history = request.form.get('medical_history')
            prediction = predict_diagnosis(symptoms, medical_history)
            return render_template('result.html', prediction=prediction)
    return render_template('predict.html')


