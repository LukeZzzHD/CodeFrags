from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from website import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    liked_comments = db.relationship('CommentLike', backref='user', lazy=True)
    liked_posts = db.relationship('PostLike', backref='user', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=1)
    role = db.relationship('Role', backref='role', lazy=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rights = db.Column(db.Integer, nullable=False, default=0)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    code = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    user_likes = db.relationship('PostLike', backref='likes', lazy=True)
    comments = db.relationship('Comment', backref='comments')
    language = db.relationship('Language', backref='language')

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_likes = db.relationship('CommentLike', backref='likes', lazy=True)
    user = db.relationship('User', backref='author')

class CommentLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

class PostLike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
