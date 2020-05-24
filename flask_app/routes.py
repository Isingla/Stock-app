from flask import render_template, url_for, flash, redirect
from flask_login import login_user,  UserMixin, logout_user, current_user, login_required
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

#app imports
from flask_app import db, app, mail_engine
from flask_app.forms import RegistrationForm, LoginForm, UpdatePassword, ForgotPassword, Input
from flask_app.models import User

@app.route("/")
def home():
    return render_template("home.html")


def send_mail(recipient, message_body):
    email=Message(
        subject="Email confirmation",
        recipients=[recipient],
        html=message_body,
        sender=app.config["MAIL_DEFAULT_SENDER"]
    )
    mail_engine.send(email)

def creates_send_email(username, first_name, last_name, email, body,redirect_function):
    encoder = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    token = encoder.dumps(username, salt=app.config['SECURITY_PASSWORD_SALT'])
    url = url_for(redirect_function, token=token, _external=True)
    message_body = f"""
    <h1>Hi, {first_name} {last_name}</h1>
    <a href="{url}">{body}</a>
    <h2>We hope to see you soon!</h2>
    """
    recipient = email
    send_mail(recipient, message_body)




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
        creates_send_email(username,first_name,last_name, email, "click to confirm you email", "confirm_user")

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

@app.route("/delete", methods=["POST"])
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for('home'))

@app.route("/confirm/<token>")
def confirm_user(token):
    decoder = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    grabbed_username = decoder.loads(token,  salt=app.config['SECURITY_PASSWORD_SALT'], max_age=7200)
    user = User.query.filter_by(username=grabbed_username).first_or_404()
    user.confiremd = True
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/update/password", methods=["GET", "POST"])
@login_required
def update_password():
    user = current_user
    old_password_form = UpdatePassword()
    if old_password_form.validate_on_submit():
        database_password = current_user.password
        form_password = old_password_form.old_password.data
        if form_password == database_password:
            return redirect(url_for("confirm_new_password"))
        else:
            flash("Password does not match", "warning")
    return render_template("old_password.html", form=old_password_form)

@app.route("/confirm/password", methods=["GET", "POST"])
def confirm_new_password():
    new_password_form = UpdatePassword()
    if new_password_form.validate_on_submit():
        current_user.password = new_password_form.password.data
        db.session.commit()
        flash("Password change successful", "success")
        return redirect(url_for("home"))
    return render_template("new_password.html", form=new_password_form)

@app.route("/admin")
@login_required
def admin_functions():
    user=User.query.all()
    if current_user.admin == True:
        return render_template("admin.html", user=user)
    else:
        flash("You do not have admin permissions", "warning")
        return redirect(url_for("home"))

@app.route("/forgot/password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPassword()
    if form.validate_on_submit():
        if form.email_username.data == "username" or form.email_username.data == "email":
            return redirect(url_for("take_input", what_selected =form.email_username.data))
        else:
            flash("please choose an input")
            return redirect(url_for("forgot_password"))
    return render_template("forgot_password.html", form=form)
@app.route("/take/input/<what_selected>", methods=["GET", "POST"])
def take_input(what_selected):
    form=Input()
    if form.validate_on_submit():
        data = form.input_field.data
        if what_selected == "username":
            user = User.query.filter_by(username=data).first()
        else:
            user = User.query.filter_by(email=data).first()
        if user is not None:
            #send an email
            email = user.email
            username=user.username
            first_name = user.first_name
            last_name = user.last_name
            creates_send_email(username,first_name,last_name,email, "click here to reset your password", "confirm_forgot_password")
            flash("We sent an email to you please click the link the reset your password", "success")


            pass
        else:
            flash(f"This,{what_selected} does not exist", "warning")
            return redirect(url_for("forgot_password"))

    return render_template('take_input.html', form=form, label=what_selected)

@app.route("/forgot/password/<token>", methods=["GET","POST"])
def confirm_forgot_password(token):
    decoder = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    grabbed_username = decoder.loads(token,  salt=app.config['SECURITY_PASSWORD_SALT'], max_age=7200)
    user = User.query.filter_by(username=grabbed_username).first_or_404()
    form=UpdatePassword()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash("Password successfully changed", "success")
        return redirect(url_for("login"))
    return render_template("new_password.html", form=form)
