from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import PatientDocument, User
from . import db
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
            # Collect symptoms and medical history from the form
            symptoms = [
                request.form.get('symptom1'),
                request.form.get('symptom2'),
                request.form.get('symptom3')
            ]
            medical_history = request.form.get('medical_history')
            
            # Ensure all symptoms and medical history are provided
            if not all(symptoms) or not medical_history:
                flash('All fields are required', 'error')
                return redirect(url_for('views.doctor_home'))
            
            # Perform prediction using the provided symptoms and medical history
            diagnosis = predict_diagnosis(symptoms, medical_history)
            
            # Return the result page with the diagnosis
            return render_template('result.html', prediction=diagnosis)
        
        return render_template('doctor_home.html')
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
        # Iterate through the submitted data
        for key in request.form.keys():
            if key.startswith('role_'):
                email = key.split('_')[1]
                role = request.form.get(key)
                
                user = User.query.filter_by(email=email).first()
                if user:
                    user.role = role
                    db.session.commit()
                    flash(f'User {user.username} ({user.email}) updated successfully', 'success')
                else:
                    flash(f'User with email {email} not found', 'error')
    
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
