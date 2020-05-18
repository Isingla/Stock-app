from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'oiwh328502jij08h2hg0hg028hg29j308gbiwpnhg08h3roiwbv08heihg8325r'
app.config['SECURITY_PASSWORD_SALT'] = 'oiwh-g0824t0?82#4-92hv0-iwgh0%2jg'

#MAIL SETTINGS

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'sayamkumar049@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ['MY_EMAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = 'sayamkumar049@gmail.com'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
mail_engine = Mail(app)

from flask_app import routes