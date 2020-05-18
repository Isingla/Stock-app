from flask_login import UserMixin

#app imports
from flask_app import db, login_manager

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
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confiremd = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"User - {self.username}, {self.email}, {self.first_name}, {self.last_name}"