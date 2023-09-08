from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileSize
from wtforms import *
from wtforms.validators import *
import datetime

class UserRegistrationForm(FlaskForm):
    firstname = StringField("First name",
                             validators = [InputRequired(message="Field required")],
                             render_kw={"class":"form-control", "placeholder":"Enter first name", "aria-label":"First name"})

    lastname = StringField("Last name", validators = [InputRequired(message="Field required")],
                            render_kw={"class":"form-control", "placeholder":"Enter last name"})
    username = StringField("Create username", validators = [InputRequired(message="Field required")],
                            render_kw={"class":"form-control", "placeholder":"Username",} )
    usertype = SelectField("User type",
                        choices=[("","--Please choose an option--"), ("student", "Student"), ("educator", "Educator"), ("parent", "Parent") ], 
                        validators=[InputRequired(message="Field required")],
                        render_kw={"class":"form-select"})

    email = EmailField("Email address",
                        validators = [InputRequired(message="Field required")],
                        render_kw={"class":"form-control", "placeholder":"name@example.com", "aria-label":"Email address"} )
    gender = SelectField("Gender Identity",

                        choices=[("","--Please choose an option--"), ("female", "Woman"), ("male", "Man"), ("other", "Other"), ("no_response", "Prefer not to say")], 
                        validators=[InputRequired(message="Field required")],
                        render_kw={"class":"form-select"})
    birthdate = DateField("Birth date", 
                          validators = [InputRequired(message="Field required")],
                          render_kw={"class":"form-control"})
    password = PasswordField("Create password",
                             validators = [InputRequired(message="Field required"), 
                                           EqualTo("password2", message="Passwords must match.")],

                             render_kw={"class":"form-control", "placeholder":"Password"})
    password2 = PasswordField("Confirm password",
                              validators = [InputRequired(message="Field required")], 
                              render_kw={"class":"form-control", "placeholder":"Password"})
    submit = SubmitField("Register", render_kw={"class":"btn button col-12" })
 
class UserLoginForm(FlaskForm):
    username = StringField("Username", render_kw={"class":"form-control", "placeholder":"Enter username"}, validators=[InputRequired(message="Username required")] )
    password = PasswordField("Password", render_kw={"class":"form-control", "placeholder":"Enter password"}, validators=[InputRequired(message="Password required")] )
    submit = SubmitField("Login", render_kw={"class":"btn button col-12"})

class DeleteForm(FlaskForm):
    user_id = StringField("user_id", render_kw={"hidden":True})
    submit = SubmitField("X", render_kw={"class":"btn btn-outline-danger", "style":"--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;"})

class UploadForm(FlaskForm):
    current_year = datetime.datetime.now().year
    resource = SelectField("Resource Name",
                           choices=[("","--Please choose an option--"), ("kcse", "Kenya Certificate of Secondary Education (KCSE)"), 
                                    ("kcpe", "Kenya Certificate of Primary Education (KCPE)"), ("mock", "Mock Exam"), 
                                    ("End Term", "End Term"), ("cat", "Continous Assessment Test (CAT)")], 
                            validators=[InputRequired(message="Field required")],
                            render_kw={"class":"form-select"})
    
    subject = SelectField("Subject",
                          choices=[("","--Please choose an option"), ("Mathematics", "Mathematics"), 
                                    ("English", "English"), ("Kiswahili", "Kiswahili"), 
                                    ("Biology", "Biology"), ("Geography", "Geography")],
                          validators=[InputRequired(message="Field required")],
                          render_kw={"class":"form-select"})
    
    school = StringField("School", validators = [InputRequired(message="Field required")],
                            render_kw={"class": "form-control", "placeholder":"Enter school"})
    
    term = SelectField("Term", 
                       choices=[("", "--Select school term"), ("KNEC", "KNEC"), ("One", "One"), ("Two", "Two"), ("Three", "Three")],
                       validators=[InputRequired(message="Field required")], 
                       render_kw={"class":"form-select"})
    
    year = IntegerField("Year (e.g 1991)", 
                        validators = [
                            InputRequired(message="Field required"),
                            NumberRange(min=1985, max=datetime.datetime.now().year, message="Invalid year.")             
                            ],
                            render_kw={"class":"form-control", "placeholder":"Enter year"})
    
    uploaded_resource = FileField("Select File to Upload", 
                       validators=[ 
                           FileRequired(message="Field required"),
                           FileAllowed(["pdf",], "Only pdf files allowed."),
                           FileSize(max_size=3145728, min_size=10, message="File size has exceeded 3MB")], 
                       render_kw={"class":"form-control", "accept": "application/pdf"})

    submit = SubmitField("Upload", render_kw={"class": "btn button col-12"})
