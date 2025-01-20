from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize, FileRequired
from wtforms import StringField, IntegerField, FileField, SelectField, EmailField, DateField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, NumberRange

class UserRegistrationForm(FlaskForm):
    first_name = StringField("First Name", 
                             validators=[InputRequired(message="Field required")],
                             render_kw={"class": "form-control", "placeholder": "Enter first name", "aria-label": "First name"})
    
    last_name = StringField("Last Name",
                            validators=[InputRequired(message="Field required")],
                            render_kw={"class": "form-control", "placeholder": "Enter last name", "aria-label": "Last name"})

    user_type = SelectField("Select User Type", 
                            choices=[("", "--Choose one--"), ("student", "Student"), ("educator", "Educator"), ("parent", "Parent/Guardian")], 
                            validators=[InputRequired(message="Field required")],
                            render_kw={"class": "form-control"})
    
    email = EmailField("Email Address",
                        validators=[InputRequired(message="Field required")],
                        render_kw={"class": "form-control", "placeholder": "name@example.com", "aria-label": "Email address"} )
    
    gender = SelectField("Gender Identity",
                        choices=[("","--Choose one--"), ("female", "Woman"), ("male", "Man"), ("other", "Other"), ("no_response", "Prefer not to say")], 
                        validators=[InputRequired(message="Field required")],
                        render_kw={"class": "form-select"})
    
    birth_date = DateField("Enter Birth Date", 
                          validators=[InputRequired(message="Field required")],
                          render_kw={"class": "form-control"})
    
    username = StringField("Create username",
                           validators=[InputRequired(message="Input required")],
                            render_kw={"class": "form-control", "placeholder": "Create username"})

    password = PasswordField("Create password",
                             validators=[InputRequired(message="Field required"), 
                                           EqualTo("password2", message="Passwords must match.")],
                             render_kw={"class": "form-control", "placeholder": "Password"})
    
    password2 = PasswordField("Confirm password",
                              validators=[InputRequired(message="Field required")], 
                              render_kw={"class": "form-control", "placeholder": "Repeat password"})
    
    submit = SubmitField("Register", render_kw={"class": "btn btn-primary col-12" })

class UserLoginForm(FlaskForm):
    username = StringField("Username", 
                           validators=[InputRequired(message="Username required")], 
                           render_kw={"class": "form-control", "placeholder": "Enter username"})
    
    password = PasswordField("Password", 
                             validators=[InputRequired(message="Password required")], 
                             render_kw={"class": "form-control", "placeholder": "Enter password"})
    submit = SubmitField("Login", render_kw={"class": "btn btn-primary col-12"})

class UploadResourceForm(FlaskForm):
    current_year = datetime.datetime.now().year
    resource = SelectField("Resource Name",
                           choices=[("","-- Please choose an option"), ("kcse", "Kenya Certificate of Secondary Education (KCSE)"), 
                                    ("kcpe", "Kenya Certificate of Primary Education (KCPE)"), ("mock", "Mock Exam"), 
                                    ("ET1", "End Term 1"),("ET2", "End Term 2"),("ET3", "End Term 3"),
                                      ("cat", "Continous Assessment Test (CAT)"), ("holiday", "HOLIDAY ASSIGNMENT")], 
                            validators=[InputRequired(message="Field required")],
                            render_kw={"class":"form-select"})
    subject = StringField("Subject", validators=[InputRequired(message="Field required")],
                            render_kw={"class":"form-control form-select", "placeholder":"Enter subject"})
    
    school = StringField("School", validators = [InputRequired(message="Field required")],
                            render_kw={"class": "form-control form-select ", "placeholder":"Enter school"})
    
    level = SelectField("Level/Class", 
                        choices=[("", "-- Select level"), ("form 1", "FORM 1"), ("form 2", "FORM 2"), ("form 3", "FORM 3"), ("form 4", "FORM 4"), ("kcse", "KCSE")],
                        validators=[InputRequired(message="Field required")],
                        render_kw={"class":"form-select"})
    
    term = SelectField("Term", 
                       choices=[("", "-- Select school term"), ("1", "One"), ("2", "Two"), ("3", "Three"), ("KCSE", "KCSE"),("mock", "MOCK")],
                       validators=[InputRequired(message="Field required")], 
                       render_kw={"class":"form-select"})
    
    year = IntegerField("Year (e.g 1991)", 
                        validators = [
                            InputRequired(message="Field required"),
                            NumberRange(min=1985, max=datetime.datetime.now() .year, message="Invalid year.")             
                            ],
                            render_kw={"class":"form-control", "placeholder":"Enter year"})
    
    uploaded_resource = FileField("Select File to Upload", 
                       validators=[ 
                           FileRequired(message="Field required"),
                           FileAllowed(["pdf",], "Only pdf files allowed."),
                           FileSize(max_size=3145728, min_size=10, message="File size has exceeded 3MB")], 
                       render_kw={"class":"form-control", "accept": "application/pdf"})

    submit = SubmitField("Upload", render_kw={"class": "btn button col-12"})