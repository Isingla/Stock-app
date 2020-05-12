from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf import FlaskForm
from wtforms.validators import EqualTo, Length, DataRequired, ValidationError
from flask_login import login_user, LoginManager, UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'oiwh328502jij08h2hg0hg028hg29j308gbiwpnhg08h3roiwbv08heihg8325r'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True)
    email = db.Column(db.String(25), unique=True)
    password = db.Column(db.String(40), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User - {self.username}, {self.email}, {self.first_name}, {self.last_name}"


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


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        password = form.password.data
        user = User(username=username, email=email,
                    first_name=first_name, last_name=last_name, password=password)
        db.session.add(user)
        db.session.commit()
        flash(f"You have succesfully registered {username}", "success")
        return redirect(url_for('home'))

    return render_template("register.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            database_password = user.password
            form_password = form.password.data
            if database_password == form_password:
                login_user(user, remember=form.remember_me.data)
                flash("Successfully logged in", "success")
                return redirect(url_for('home'))
            else:
                flash(f"Password is incorrect", "warning")
        else:
            flash(f"Username is incorrect", "warning")
    return render_template("login.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
