from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class StudentRegistrationForm(FlaskForm):
    firstname = StringField("First name", validators = [InputRequired(message="Field required")], render_kw={"class": "form-control"})
    lastname = StringField("Last name", validators = [InputRequired(message="Field required")], render_kw={"class": "form-control"})
    username = StringField("Username", validators = [InputRequired(message="Field required")], render_kw={"class":"form-control"} )
    email = EmailField("Email address", validators = [InputRequired(message="Field required")], render_kw={"class":"form-control"} )
    gender = SelectField("Gender Identity",
                        choices=[("","--Please choose an option--"), ("female", "Woman/She/Her"), ("male", "Man/He/Him"), ("trans", "Trans"), 
                                  ("non-binary", "Non-binary/non-conforming"), ("no_response", "Prefer not to respond")], 
                        validators=[InputRequired(message="Field required")],
                        render_kw={"class":"form-select"})
    birthdate = DateField("Birth date", 
                          validators = [InputRequired(message="Field required")],
                          render_kw={"class":"form-control"})
    password = PasswordField("Create password",
                             validators = [InputRequired(message="Field required"), 
                                           EqualTo("password2", message="Passwords must match.")],
                             render_kw={"class":"form-control"})
    password2 = PasswordField("Confirm password",
                              validators = [InputRequired(message="Field required")], 
                              render_kw={"class":"form-control"})
    submit = SubmitField("Register", render_kw={"class":"btn btn-primary"})

class StudentLoginForm(FlaskForm):
    username = StringField("Username", render_kw={"class":"form-control"}, validators=[InputRequired(message="Username required")] )
    password = PasswordField("Password", render_kw={"class":"form-control"}, validators=[InputRequired(message="Password required")] )
    submit = SubmitField("Login", render_kw={"class":"btn btn-primary"})


class DeleteForm(FlaskForm):
    student_id = StringField("student_id",)
    submit = SubmitField("Delete", render_kw={"style": "background-color:red", "style":"border:none"})