from flask import render_template, url_for, flash, redirect
from flask_login import login_user,  UserMixin, logout_user, current_user, login_required

#app imports
from flask_app import db, app
from flask_app.forms import RegistrationForm, LoginForm
from flask_app.models import User

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

@app.route("/logout", methods=["GET"])
def logout():
    if  current_user.is_authenticated:
        logout_user()
        flash("Successfully logged out", "success")
    else:
        flash("User not logged in", "warning")
    return redirect(url_for('home'))

@app.route("/profile")
@login_required
def my_profile():
    return render_template("profile.html", user=current_user)