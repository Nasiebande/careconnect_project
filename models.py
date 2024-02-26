from flask_sqlalchemy import SQLAlchemy

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
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    care_needed = db.Column(db.String(100))
    # Add more fields as needed for patient information

class Caregiver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    experience = db.Column(db.String(100))
    services_offered = db.Column(db.String(100))
    # Add more fields as needed for caregiver information

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)
    patient = db.relationship('Patient', backref='appointments')
    caregiver = db.relationship('Caregiver', backref='appointments')
    date_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)
    care_requirements = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=False)  # Additional field for location

    def __repr__(self):
        return f'<Appointment {self.id}>'
    
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)  # Foreign key to Patient model
    caregiver_id = db.Column(db.Integer, db.ForeignKey('caregiver.id'), nullable=False)  # Foreign key to Caregiver model
    rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Review {self.id}>'