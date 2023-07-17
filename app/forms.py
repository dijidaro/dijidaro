from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class StudentRegistrationForm(FlaskForm):
    firstname = StringField("First name", [validators.input_required(message="Field required")], render_kw={"class": "form-control"})
    lastname = StringField("Last name", validators = [InputRequired(message="Field required")], render_kw={"class": "form-control"})
    username = StringField("Username", render_kw={"class":"form-control"} )
    email = EmailField("Email address", render_kw={"class":"form-control"} )
    gender = SelectField("Gender Identity",
                         validators = [InputRequired(message="Field required")], 
                         render_kw={"class":"form-select", "aria-label":"Gender selection"},
                         choices=[("default","Select"), ("female", "Woman/She/Her"), ("male", "Man/He/Him"), ("trans", "Trans"), 
                                  ("non-binary", "Non-binary/non-conforming"), ("no_response", "Prefer not to respond")])
    birthdate = DateField("Birth date", 
                          validators = [InputRequired(message="Field required")],
                          render_kw={"class":"form-control"})
    password = PasswordField("Create password",
                             validators = [InputRequired(message="Field required")],
                             render_kw={"class":"form-control"})
    password2 = PasswordField("Confirm password",
                              validators = [InputRequired(message="Field required")], 
                              render_kw={"class":"form-control"})
    submit = SubmitField("Register", render_kw={"class":"btn btn-primary"})

class StudentLoginForm(FlaskForm):
    username = StringField("Username", render_kw={"class":"form-control"}, validators=[InputRequired(message="Username required")] )
    password = PasswordField("Password", render_kw={"class":"form-control"}, validators=[InputRequired(message="Password required")] )
    submit = SubmitField("Login", render_kw={"class":"btn btn-primary"})

