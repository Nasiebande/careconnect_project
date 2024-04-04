from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime


db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    user_type = db.Column(db.String(20))  # 'patient' or 'caregiver'
    phone_number = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    location = db.Column(db.String(255))
    
    # Define the relationship with Patient and Caregiver models
    def create_patient_profile(self):
        if not self.patient:
            self.patient = Patient()
            db.session.add(self.patient)
            db.session.commit()
    
    def create_caregiver_profile(self):
        if not self.caregiver:
            self.caregiver = Caregiver()
            db.session.add(self.caregiver)
            db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def update_profile(self, name, email, date_of_birth, gender, location, phone_number):
        from dateutil.relativedelta import relativedelta    

        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.location = location
        self.age = relativedelta(datetime.today(), self.date_of_birth).years if self.date_of_birth else None         

    def is_profile_complete(self):
        # Logic to check if the user's profile is complete
        # For example, you could check if all required fields are filled
        if self.name and self.email and self.phone_number:
            return True
        else:
            return False
    
    def __repr__(self):
        return f'<User {self.name}>'

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  
    care_needed = db.Column(db.String(100), nullable=False)  # Changing care_needed to a single field
    preferences = db.Column(db.String(100))  # Add preferences field
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Patient {self.name}>'

class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    experience = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    license_number = db.Column(db.String(100))
    services_offered = db.Column(db.String(100))
    license_verified = db.Column(db.Boolean, default=False)  # New field for license verification status
    verification_error = db.Column(db.String(255))  # New field for storing verification error message

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
    