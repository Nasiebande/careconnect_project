from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from models import db, User, Patient, Caregiver, Appointment, Review

load_dotenv()  # Load environment variables from .env file

# Create Flask Instance
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('SECRET_KEY')

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///careconnect.db'

# Suppress deprecation warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Use the db instance from models.py
db.init_app(app)

def process_payment(amount):
    # Placeholder logic for payment processing
    # Here, you can simulate a successful payment
    return 'success'

# Define your routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

# Registration route for patients
@app.route('/register/patient', methods=['POST'])
def register_patient():
    if request.method == 'POST':
        # Extract form data
        patient_name = request.form['patient_name']
        patient_email = request.form['patient_email']
        patient_phone = request.form['patient_phone']
        patient_location = request.form['patient_location']
        condition = request.form['condition']
        care_needed = request.form.getlist('care_needed')  # Assuming care_needed is a list of selected care needs
        
        # Create a new patient instance
        new_patient = Patient(name=patient_name, email=patient_email, phone_number=patient_phone, location=patient_location, condition=condition, care_needed=care_needed)
        
        # Add the patient to the database
        db.session.add(new_patient)
        db.session.commit()
        
        flash('Patient registration successful', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/register/caregiver', methods=['GET', 'POST'])
def register_caregiver():
    if request.method == 'POST':
        # Handle caregiver registration form submission
        caregiver_name = request.form['caregiver_name']
        caregiver_email = request.form['caregiver_email']
        caregiver_phone = request.form['caregiver_phone']  # Extract phone number
        caregiver_location = request.form['caregiver_location']
        qualification = request.form['qualification']
        experience = request.form['experience']
        services_offered = request.form.getlist('services_offered')
        
        # Process the data as needed (e.g., store in the database)
        caregiver = Caregiver(name=caregiver_name, email=caregiver_email, phone=caregiver_phone, location=caregiver_location, qualification=qualification, experience=experience, services_offered=services_offered)
        
        db.session.add(caregiver)
        db.session.commit()
        flash('Caregiver registration successful', 'success')
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database to check if the username exists
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):  # Assuming you have a method to check the password
            # If the credentials are correct, set the user as logged in
            session['logged_in'] = True
            session['user_id'] = user.id  # Store the user ID in the session
            return redirect(url_for('home'))  # Redirect to the home page or another route
        else:
            # If the credentials are incorrect, render the login form again with an error message
            return render_template('login.html', error='Invalid username or password')

    # If the request method is GET, render the login form
    return render_template('login.html', error=None)

# Caregiver Search route
@app.route('/search_caregivers', methods=['GET', 'POST'])
def search_caregivers():
    if request.method == 'POST':
        patient_requirements = request.form['patient_requirements']
        matching_caregivers = Caregiver.query.filter(Caregiver.qualifications.contains(patient_requirements)).all()
        return render_template('caregivers_results.html', caregivers=matching_caregivers)
    return render_template('search_caregivers.html')

@app.route('/select_caregiver', methods=['POST'])
def select_caregiver():
    if request.method == 'POST':
        caregiver_id = request.form.get('caregiver_id')  # Assuming caregiver_id is submitted from the form
        caregiver = Caregiver.query.get(caregiver_id)
        if caregiver:
            
            return "Caregiver selected successfully"
        else:
            return "Caregiver not found"
        
@app.route('/schedule_appointment', methods=['GET', 'POST'])
def schedule_appointment():
    if request.method == 'POST':
        # Get form data
        patient_id = request.form['patient_id']
        caregiver_id = request.form['caregiver_id']
        date_time_str = request.form['date_time']
        duration = float(request.form['duration'])  # Convert to float

        # Find the caregiver and patient by ID
        caregiver = Caregiver.query.get(caregiver_id)
        patient = Patient.query.get(patient_id)

        # Create a new appointment
        appointment = Appointment(
            patient_id=patient.id,
            caregiver_id=caregiver.id,
            date_time=datetime.strptime(date_time_str, "%Y-%m-%d %H:%M"),
            duration=duration
        )

        # Add appointment to the database
        db.session.add(appointment)
        db.session.commit()

        # Redirect to home page or display success message
        return redirect(url_for('home'))

    # Render the appointment scheduling form
    return render_template('schedule_appointment.html')

@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    if request.method == 'POST':
        # Get the appointment ID from the form data
        appointment_id = request.form['appointment_id']
        
        # Retrieve the appointment object from the database using the ID
        appointment = Appointment.query.get(appointment_id)
        
        if appointment:
            # Process payment (placeholder)
            appointment.payment_status = True  # Update payment status to True
            
            # Commit changes to the database
            db.session.commit()
            
            # Redirect to a success page
            return redirect(url_for('payment_success'))
        else:
            # If appointment ID is not found, redirect to an error page
            return redirect(url_for('payment_error'))
        
@app.route('/confirm_and_pay', methods=['GET', 'POST'])
def confirm_and_pay():
    if request.method == 'POST':
        # Retrieve form data
        patient_name = request.form['patient_name']
        caregiver_name = request.form['caregiver_name']
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        appointment_duration = request.form['appointment_duration']
        payment_amount = request.form['payment_amount']
        
        # Perform payment processing (placeholder)
        payment_status = process_payment(payment_amount)
        
        # If payment is successful, proceed to scheduling appointment
        if payment_status == 'success':
            appointment = Appointment(patient_name, caregiver_name, appointment_date, appointment_time, appointment_duration)
            # Save the appointment to the database or perform any other necessary actions
            return redirect(url_for('payment_status', success='true'))
        else:
            return redirect(url_for('payment_status', success='false'))
    
    # If request method is GET, render the confirmation form
    return render_template('confirm_and_pay.html') 

# Route to cancel an appointment
@app.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    # Retrieve the appointment from the database using the appointment ID
    appointment = Appointment.query.get(appointment_id)
    
    if appointment:
        # Delete the appointment from the database
        db.session.delete(appointment)
        db.session.commit()
        
        # Redirect to a success page
        return redirect(url_for('cancel_success'))
    else:
        # If appointment ID is not found, redirect to an error page
        return redirect(url_for('cancel_error'))       

@app.route('/payment_status')
def payment_status():
    success = request.args.get('success')
    return render_template('payment_status.html', success=success)

@app.route('/dispatch_caregiver/<int:appointment_id>', methods=['POST'])
def dispatch_caregiver(appointment_id):
    if request.method == 'POST':
        # Retrieve the appointment object from the database using the appointment ID
        appointment = Appointment.query.get(appointment_id)
        
        if appointment:
            # Retrieve a caregiver from the database based on certain criteria (e.g., availability)
            caregiver = Caregiver.query.filter_by(availability=True).first()

            if caregiver:
                # Assign the selected caregiver to the appointment
                appointment.caregiver = caregiver

                # Update the appointment status to "Dispatched"
                appointment.status = "Dispatched"

                # Commit changes to the database
                db.session.commit()

                # Redirect to a success page
                return redirect(url_for('dispatch_success'))
            else:
                # If no caregiver is available, redirect to an error page
                return redirect(url_for('dispatch_status', success='true'))
        else:
            # If appointment ID is not found, redirect to an error page
            return redirect(url_for('dispatch_status', success='false'))

@app.route('/dispatch_status/<string:success>')
def dispatch_status(success):
    return render_template('dispatch_status.html', success=success)

@app.route('/caregiving_session/<int:appointment_id>')
def caregiving_session(appointment_id):
    # Retrieve the appointment object from the database using the appointment ID
    appointment = Appointment.query.get(appointment_id)

    if appointment:
        # Render the caregiving session template and pass the appointment object to it
        return render_template('caregiving_session.html', appointment=appointment)
    else:
        # If appointment ID is not found, render an error template
        return render_template('error.html', message='Appointment not found')
    
@app.route('/complete_and_feedback/<int:appointment_id>', methods=['GET', 'POST'])
def complete_and_feedback(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)

    if request.method == 'POST':
        appointment.status = 'Completed'
        appointment.feedback = request.form.get('feedback')

        # Create a new review object
        review = Review(
            reviewer_id=session['user_id'],  # Assuming you have user authentication
            reviewed_entity_id=appointment.caregiver_id,
            rating=int(request.form.get('rating')),  # Assuming rating is provided in the form
            comments=request.form.get('comments')
        )
        db.session.add(review)
        db.session.commit()

        return redirect(url_for('feedback_success'))

    return render_template('complete_and_feedback.html', appointment=appointment)

if __name__ == '__main__':
    app.run(debug=True)