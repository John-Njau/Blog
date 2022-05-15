from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class Crud:
    def save(self):
        db.session.add(self)
        db.session.commit()
        return True
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True


@login_manager.user_loader
def user_loader(user_id):
    return Users.query.get(int(user_id))
    

class Users(UserMixin, db.Model, Crud):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_image_path = db.Column(db.String(255))
    blog = db.relationship('Blog', backref='blogs', lazy=True)
    user_created = db.Column(db.DateTime, default=datetime.now())
    user_updated = db.Column(db.DateTime, onupdate=datetime.now())
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Blog(db.Model, Crud):
    __tablename__ = "blog"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    blog = db.Column(db.String(1500), nullable=False)
    comments = db.relationship('Comments', backref='comments', lazy=True)
    likes = db.relationship('Likes', backref='likes', lazy=True)
    poster_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    blog_created = db.Column(db.DateTime, default=datetime.now())
    blog_updated = db.Column(db.DateTime, onupdate=datetime.now())

class Comments(db.Model, Crud):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    comment_created = db.Column(db.DateTime, default=datetime.now())
    comment_updated = db.Column(db.DateTime, onupdate=datetime.now())
    
class Likes(db.Model, Crud):
    __tablename__ = "likes"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    
class Subscriptions(db.Model, Crud):
    __tablename__ = "subscriptions"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.now())


class Photos(db.Model, Crud):
    __tablename__ = "photos"
    
    id = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String(255), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    img_uploaded = db.Column(db.DateTime, default=datetime.now())
    
    
