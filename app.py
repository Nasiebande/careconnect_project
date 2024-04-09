from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
import os
from flask_migrate import Migrate
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from models import db, User, Patient, Caregiver, Appointment, Review
from forms import RegistrationForm, PatientRegistrationForm, CaregiverRegistrationForm, ProfileForm, AppointmentForm

load_dotenv()  # Load environment variables from .env file

# Create Flask Instance
app = Flask(__name__, template_folder='templates', static_folder='static')

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.secret_key = os.getenv('SECRET_KEY')

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///careconnect.db'

# Suppress deprecation warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Use the db instance from models.py
db.init_app(app)

migrate = Migrate(app, db)

def process_payment(amount):
    # Placeholder logic for payment processing
    return 'success'

# Define your routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Check if user already exists
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address is already registered. Please use a different one.', 'error')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(form.password.data)

        # Create a new user if user does not exist
        new_user = User(name=form.name.data,
                        email=form.email.data,
                        password=hashed_password,
                        user_type=form.user_type.data,
                        gender=form.gender.data,
                        date_of_birth=form.date_of_birth.data,
                        location=form.location.data,
                        phone_number=form.phone_number.data)
        db.session.add(new_user)
        db.session.commit()

        flash("User signed up successfully!")

        # Redirect to either patient or caregiver registration based on user type
        if form.user_type.data == 'caregiver':
            return redirect(url_for('register_caregiver'))
        elif form.user_type.data == 'patient':
            return redirect(url_for('register_patient'))
        else:
            flash('Invalid user type selected.', 'error')
            return redirect(url_for('signup'))

    return render_template('signup.html', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Query the database to check if the username exists
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):  # Check hashed password
            # If the credentials are correct, set the user as logged in
            login_user(user)  # Use Flask-Login's login_user function
            flash('Logged in successfully!', 'success')

            # Redirect the user to the appropriate dashboard based on user type
            if user.user_type == 'patient':
                return redirect(url_for('patient_dashboard'))
            elif user.user_type == 'caregiver':
                return redirect(url_for('caregiver_dashboard'))
        
        # If the credentials are incorrect, render the login form again with an error message
        flash('Invalid email or password.', 'error')
        return render_template('login.html')

    # If the request method is GET, render the login form
    return render_template('login.html', error=None)


@app.route('/logout')
def logout():
    logout_user()  # Log out the current user using Flask-Login's logout_user function
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Registration route for patients
@app.route('/register/patient', methods=['GET', 'POST'])
@login_required
def register_patient():
    form = PatientRegistrationForm()
    
    # Debug statement to check if form is submitted
    print("Form submitted:", form.is_submitted())
    
    if form.validate_on_submit():
        # Debug statement to indicate form validation passed
        print("Form validation passed")

        # Create a new patient associated with the logged-in user
        patient = Patient(
            user_id=current_user.id,
            name=form.patient_name.data,
            email=form.patient_email.data,
            phone_number=form.phone_number.data,  
            condition=form.condition.data,
            location=form.patient_location.data,
            gender=form.gender.data,
            care_needed=form.care_needed.data,
            preferences=form.preferences.data
        )
        db.session.add(patient)
        db.session.commit()
        flash('Patient registration successful', 'success')
        return redirect(url_for('patient_dashboard'))
    
    # Debug statement to print form errors if validation fails
    print("Form errors:", form.errors)
    
    return render_template('register_patient.html', form=form)

def mock_verify_license(license_path):
    # Placeholder for mock verification process
    # You can customize this function as needed
    if license_path:
        flash('License verification successful', 'success')
        return True
    else:
        flash('License verification failed', 'error')
        return False

@app.route('/register/caregiver', methods=['GET', 'POST'])
def register_caregiver():
    form = CaregiverRegistrationForm()
    
    # Debug statement to check if form is submitted
    print("Form submitted:", form.is_submitted())
    
    if form.validate_on_submit():
        # Debug statement to indicate form validation passed
        print("Form validation passed")
        
        # Process the data as needed
        license_number = form.license_number.data
        print("License number:", license_number)

        # Perform mock verification using the license number
        license_verified = mock_verify_license(license_number)
        print("License verification result:", license_verified)

        # Convert list of selected services to a comma-separated string
        services_offered = ', '.join(form.services_offered.data)

        # Create a new caregiver instance
        caregiver = Caregiver(
            user_id=current_user.id,
            name=form.caregiver_name.data,
            email=form.caregiver_email.data,
            phone_number=form.phone_number.data,
            location=form.caregiver_location.data,
            qualification=form.qualification.data,
            experience=form.experience.data,
            gender=form.gender.data,
            license_verified=license_verified,  # Update license_verified field
            services_offered=services_offered
        )

        # Add the caregiver to the database
        db.session.add(caregiver)
        db.session.commit()

        flash('Caregiver registration successful', 'success')
        return redirect(url_for('caregiver_dashboard'))
    
    # Debug statement to print form errors if validation fails
    print("Form errors:", form.errors)
    
    return render_template('register_caregiver.html', form=form)
    
@app.route('/patient_dashboard')
@login_required
def patient_dashboard():
    if current_user.user_type == 'patient':
        return render_template('patient_dashboard.html', user_name=current_user.name)
    else:
        flash('You do not have access to the patient dashboard.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/caregiver_dashboard')
@login_required
def caregiver_dashboard():
    if current_user.user_type == 'caregiver':
        return render_template('caregiver_dashboard.html', user_name=current_user.name, license_verified=True)  # Set license_verified as needed
    else:
        flash('You do not have access to the caregiver dashboard.', 'error')
        return redirect(url_for('dashboard'))
    
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()

    # Check if the user has already filled their profile details
    if not current_user.is_profile_complete():
        # Redirect the user to the profile update page
        return redirect(url_for('update_profile'))

    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        # Update other profile fields as needed

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    # Prepopulate the form fields with the user's current information
    form.name.data = current_user.name
    form.email.data = current_user.email
    form.phone_number.data = current_user.phone_number
    # Prepopulate other form fields with the user's current information

    return render_template('profile.html', form=form, user_name=current_user.name)

@app.route('/appointments')
@login_required
def appointments():
    form = AppointmentForm() 

    if current_user.user_type == 'patient':
        # For patients, filter appointments based on patient ID
        upcoming_appointments = Appointment.query.filter_by(patient_id=current_user.id).filter(Appointment.date_time > datetime.now()).all()
    elif current_user.user_type == 'caregiver':
        # For caregivers, filter appointments based on caregiver ID
        upcoming_appointments = Appointment.query.filter_by(caregiver_id=current_user.id).filter(Appointment.date_time > datetime.now()).all()
    else:
        return redirect(url_for('index'))  # Redirect to home if user type is not patient or caregiver
    
    return render_template('appointments.html', upcoming_appointments=upcoming_appointments, form=form)  # Pass the form variable to the template

@app.route('/book_appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=current_user.id if current_user.user_type == 'patient' else form.patient_id.data,
            caregiver_id=form.caregiver_id.data,
            date_time=form.date_time.data,
            duration=form.duration.data,
            location=form.location.data,
            notes=form.notes.data
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('appointments'))
    
    return render_template('book_appointment.html', form=form)

@app.route('/view_appointment/<int:appointment_id>')
@login_required
def view_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        flash('Appointment not found!', 'error')
        return redirect(url_for('appointments'))

    return render_template('view_appointment.html', appointment=appointment)

@app.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_specific_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        flash('Appointment not found!', 'error')
        return redirect(url_for('appointments'))

    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment canceled successfully!', 'success')
    return redirect(url_for('appointments'))

@app.route('/reschedule_appointment/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def reschedule_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if not appointment:
        flash('Appointment not found!', 'error')
        return redirect(url_for('appointments'))

    form = AppointmentForm(obj=appointment)
    if form.validate_on_submit():
        appointment.date_time = form.date_time.data
        appointment.duration = form.duration.data
        appointment.location = form.location.data
        appointment.notes = form.notes.data
        db.session.commit()
        flash('Appointment rescheduled successfully!', 'success')
        return redirect(url_for('appointments'))
    
    return render_template('reschedule_appointment.html', form=form, appointment=appointment)
    
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
    with app.app_context():
        # Create all database tables
        db.create_all()
    app.run(debug=True)