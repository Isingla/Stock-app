from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import EqualTo, Length, DataRequired, ValidationError

# app imports
from flask_app.models import User





class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[
                           Length(max=12), DataRequired()])
    email = StringField("Email", validators=[Length(max=25), DataRequired()])
    first_name = StringField("First Name", validators=[
                             Length(max=20), DataRequired()])
    last_name = StringField("Last Name", validators=[
                            Length(max=20), DataRequired()])

    password = PasswordField("Password", validators=[
                             Length(max=40), DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[EqualTo("password", message="Passwords must match"), DataRequired()])
    submit = SubmitField("Sign Up")


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Choose a unique username")


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "There is an account made with that email already")

class LoginForm(FlaskForm):
    username= StringField("Username", validators=[DataRequired()])
    password= PasswordField("Password", validators=[DataRequired()])
    remember_me= BooleanField("Remember Me")
    submit_login= SubmitField("Login")


class  UpdatePassword(FlaskForm):
    old_password = PasswordField("Previous Password", validators=[
                             Length(max=40)])
    password = PasswordField("Password", validators=[
                             Length(max=40)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[EqualTo("password", message="Passwords must match")])
    submit_new_password = SubmitField("Submit")

class ForgotPassword(FlaskForm):
    email_username = RadioField("Select what you remember", choices=[("username", "Username"), ("email", "Email")])
    submit = SubmitField("Submit")


