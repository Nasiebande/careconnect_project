from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(20))  # 'patient' or 'caregiver'
    
    # Define the relationship with Patient and Caregiver models
    patient = db.relationship('Patient', backref='user', uselist=False)
    caregiver = db.relationship('Caregiver', backref='user', uselist=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)  # Adding phone number field
    condition = db.Column(db.String(100), nullable=False)  # Adding condition field
    location = db.Column(db.String(100), nullable=False)
    care_needed = db.Column(db.String(100), nullable=False)  # Changing care_needed to a single field
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Patient {self.name}>'

class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))  # Add email attribute
    phone_number = db.Column(db.String(20), nullable=False)  # Adding phone number field
    location = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    experience = db.Column(db.String(100))
    # Define a relationship with a new table for services offered
    services_offered = db.relationship('ServiceOffered', secondary='caregiver_service_offered', backref='caregivers')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Caregiver {self.name}>'

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)
    patient = db.relationship('Patient', backref='appointments_as_patient', foreign_keys=[patient_id])
    caregiver = db.relationship('Caregiver', backref='appointments_as_caregiver', foreign_keys=[caregiver_id])
    date_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)
    care_requirements = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Appointment {self.id}>'
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Review {self.id}>'
