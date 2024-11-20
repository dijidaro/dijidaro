from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, EmailField, DateField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo

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
