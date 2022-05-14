from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

from . import db

dt = datetime.date()


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # bio = db.Column(db.String(255))
    # profile_image_path = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, value):
        self.password_hash = Bcrypt.generate_password_hash(value)

    def verify_password(self, value):
        return Bcrypt.check_password_hash(self.password_hash, value)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'{self.username}'
