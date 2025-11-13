from . import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    locale = db.Column(db.String(8), default=None)

    def __repr__(self):
        return "<User {}>".format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
