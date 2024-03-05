from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, SubmitField, PasswordField, FileField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField('User Type', choices=[('patient', 'Patient'), ('caregiver', 'Caregiver')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class PatientRegistrationForm(FlaskForm):
    patient_name = StringField('Name', validators=[DataRequired()])
    patient_email = StringField('Email', validators=[DataRequired(), Email()])
    patient_number = StringField('Phone Number', validators=[DataRequired()])
    condition = StringField('Condition', validators=[DataRequired()])
    patient_location = StringField('Location', validators=[DataRequired()])
    sex = StringField('Sex', validators=[DataRequired()])
    care_needed = StringField('Care Needed', validators=[DataRequired()])
    preferences = StringField('Preferences')
    user_type = SelectField('User Type', choices=[('patient', 'Patient')], validators=[DataRequired()])
    submit = SubmitField('Register as Patient')

class CaregiverRegistrationForm(FlaskForm):
    caregiver_name = StringField('Name', validators=[DataRequired()])
    caregiver_email = StringField('Email', validators=[DataRequired(), Email()])
    caregiver_phone = StringField('Phone Number', validators=[DataRequired()])
    caregiver_location = StringField('Location', validators=[DataRequired()])
    qualification = StringField('Qualification', validators=[DataRequired()])
    experience = StringField('Experience', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    license = FileField('Upload License', validators=[DataRequired()])
    
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
    
    user_type = SelectField('User Type', choices=[('caregiver', 'Caregiver')], validators=[DataRequired()])
    submit = SubmitField('Register as Caregiver')        