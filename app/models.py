from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
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


class User(UserMixin, db.Model, Crud):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String(255))
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

    @login_manager.user_loader
    def user_loader(user_id):
        return User.query.get(int(user_id))

    def add_comment(self, comment):
        self.comments.append(comment)
        return self.save()

    def add_blog(self, blog):
        self.blogs.append(blog)
        return self.save()


class Blog(db.Model, Crud):
    __tablename__ = "blog"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    blog = db.Column(db.String(1500), nullable=False)
    blog_pic = db.Column(db.String(255))
    comments = db.relationship('Comment', backref='comments', lazy=True)
    likes = db.relationship('Likes', backref='like', lazy=True)
    dislikes = db.relationship('Dislikes', backref='dislike', lazy=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    blog_created = db.Column(db.DateTime, default=datetime.now())
    
    blog_updated = db.Column(db.DateTime, onupdate=datetime.now())

    def delete(self):
        user = User.query.filter_by(id=self.author).first()
        user.blogs.remove(self)
        self.delete()
        return self.save()

    def update(self):
        blog = Blog.query.filter_by(id=self.id).first()
        blog.blog = self.blog
        return blog.save()

    def __repr__(self):
        return self.blog


class Comment(db.Model, Crud):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    comment_created = db.Column(db.DateTime, default=datetime.now())
    comment_updated = db.Column(db.DateTime, onupdate=datetime.now())

    def delete(self):
        blog = Blog.query.filter_by(id=self.blog).first()
        blog.comments.remove(self)
        self.delete()
        return self.save()

    def update(self):
        comment = Comment.query.filter_by(id=self.id).first()
        comment.comment = self.comment
        return comment.save()

    def __repr__(self):
        self.comment


class Likes(db.Model, Crud):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    likes = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

    def like(self, id):
        like_blog = Likes(user=current_user, blog_id=id)
        like_blog.save_like()

    @classmethod
    def get_like(cls, id):
        like = Likes.query.filter_by(blog_id=id).all()
        return like

    @classmethod
    def all_likes(cls):
        likes = Likes.query.order_by('id').all()
        return likes


class Dislikes(db.Model, Crud):
    __tablename__ = "dislikes"

    id = db.Column(db.Integer, primary_key=True)
    dislikes = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

    def dislike(self, id):
        dislike_blog = Dislikes(user=current_user, blog_id=id)
        dislike_blog.save_dislike()

    @classmethod
    def get_dislike(cls, id):
        dislike = Dislikes.query.filter_by(blog_id=id).all()
        return dislike

    @classmethod
    def all_dislikes(cls):
        dislikes = Dislikes.query.order_by('id').all()
        return dislikes


class Subscriptions(db.Model, Crud):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.now())


class Photos(db.Model, Crud):
    __tablename__ = "photos"

    id = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String(255), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    img_uploaded = db.Column(db.DateTime, default=datetime.now())


class Quote:
    def __init__(self, id, author, quote, url):
        self.id = id
        self.author = author
        self.quote = quote
        self.url = url
