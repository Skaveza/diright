from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import PatientDocument, User
from . import db
import pandas as pd
from .patient_utils import create_new_patient
from .ml_module import predict_diagnosis

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.role == 'doctor':
            return redirect(url_for('views.doctor_home'))
        elif current_user.role == 'admin':
            return redirect(url_for('views.admin_home'))
    return render_template('home.html')

@views.route('/doctor', methods=['GET', 'POST'])
@login_required
def doctor_home():
    if current_user.role == 'doctor':
        if request.method == 'POST':
            patient_id = request.form.get('patient_id')
            if not patient_id:
                return redirect(url_for('views.new_patient'))
            symptoms = [
                request.form.get('symptom1'),
                request.form.get('symptom2'),
                request.form.get('symptom3')
            ]
            patient = PatientDocument.query.filter_by(patient_id=patient_id).first()
            if patient:
                medical_history = patient.medical_history
                diagnosis = predict_diagnosis(symptoms, medical_history)
                patient.symptoms = ", ".join(symptoms)
                patient.diagnosis = diagnosis
                db.session.commit()
                flash('Diagnosis updated successfully', 'success')
                return render_template('result.html', prediction=diagnosis, patient=patient)
            else:
                flash('Patient not found', 'error')
                return redirect(url_for('views.new_patient'))
        return render_template('doctor_home.html')
    return redirect(url_for('views.home'))

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
            return render_template('patient.html', document=document)
        else:
            flash('No documents found for this patient ID', 'error')
            return redirect(url_for('views.doctor_home'))
    return redirect(url_for('views.home'))

@views.route('/result')
@login_required
def result():
    if current_user.role == 'doctor':
        return render_template('result.html')
    return redirect(url_for('views.home'))

@views.route('/admin')
@login_required
def admin_home():
    if current_user.role == 'admin':
        return render_template('admin_home.html')
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

@views.route('/update_database', methods=['GET', 'POST'])
@login_required
def update_database():
    if current_user.role == 'admin':
        if request.method == 'POST':
            patient_id = request.form.get('patient_id')
            medical_history = request.form.get('medical_history')
            patient = PatientDocument.query.filter_by(patient_id=patient_id).first()
            if patient:
                patient.medical_history = medical_history
                db.session.commit()
                flash('Patient medical history updated successfully', 'success')
            else:
                new_patient = PatientDocument(patient_id=patient_id, medical_history=medical_history)
                db.session.add(new_patient)
                db.session.commit()
                flash('New patient added to database', 'success')
        return render_template('update_database.html')
    return redirect(url_for('views.home'))
