from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'oiwh328502jij08h2hg0hg028hg29j308gbiwpnhg08h3roiwbv08heihg8325r'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

from flask_app import routes