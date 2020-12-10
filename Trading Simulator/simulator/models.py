from datetime import datetime

from flask_login import UserMixin

from simulator import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    hashed_pwd = db.Column(db.String())
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User - {self.id}, {self.username}, {self.password}, {self.hashed_pwd}, {self.email}, {self.date_created}"
