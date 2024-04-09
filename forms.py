from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField, PasswordField, IntegerField, DateField, DateTimeField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[('caregiver', 'Caregiver'), ('patient', 'Patient')], validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')


class PatientRegistrationForm(FlaskForm):
    patient_name = StringField('Name', validators=[DataRequired()])
    patient_email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    condition = StringField('Condition', validators=[DataRequired()])
    patient_location = StringField('Location', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    care_needed = StringField('Care Needed', validators=[DataRequired()])
    preferences = StringField('Preferences')
    submit = SubmitField('Register as Patient')

class CaregiverRegistrationForm(FlaskForm):
    caregiver_name = StringField('Name', validators=[DataRequired()])
    caregiver_email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    caregiver_location = StringField('Location', validators=[DataRequired()])
    qualification = StringField('Qualification', validators=[DataRequired()])
    experience = StringField('Experience', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    license_number = StringField('License Number', validators=[DataRequired()])
    
    # Define choices for the services offered
    SERVICES_CHOICES = [
        ('Post surgery', 'Post surgery'),
        ('Bed-ridden care', 'Bed-ridden care'),
        ('Terminally ill care', 'Terminally ill care'),
        ('General convalescents', 'General convalescents'),
        ('Palliative care', 'Palliative care'),
        ('Bathing and personal hygiene', 'Bathing and personal hygiene'),
        ('Feeding', 'Feeding'),
        ('Ambulation', 'Ambulation'),
        ('Administering prescribed medication', 'Administering prescribed medication'),
        ('Overnight Elderly Care', 'Overnight Elderly Care'),
        ('Maternal and child care', 'Maternal and child care')
    ]
    services_offered = SelectMultipleField('Services Offered', choices=SERVICES_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Register as Caregiver')

class ProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Update Profile')

class AppointmentForm(FlaskForm):
    date_time = DateTimeField('Date and Time', validators=[DataRequired()], format='%Y-%m-%d %H:%M:%S')
    duration = IntegerField('Duration (minutes)', validators=[DataRequired()])
    notes = TextAreaField('Additional Notes')
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')      
        