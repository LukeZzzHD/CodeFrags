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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    postID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    code = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    fk_tag = db.Column(db.Integer, db.ForeignKey('tag.tagID'))
    fk_user = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

class Language(db.Model):
    languageID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)

class Tag(db.Model):
    tagID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

class Comment(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fk_Post = db.Column(db.Integer, db.ForeignKey('post.postID'), nullable=False)
    fk_User = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

class PostLanguage(db.Model):
    post_language_id = db.Column(db.Integer, primary_key=True)
    fk_Post = db.Column(db.Integer, db.ForeignKey('post.postID'), nullable=False)
    fk_Language = db.Column(db.Integer, db.ForeignKey('language.languageID'), nullable=False)

class PostLike(db.Model):
    post_like_id = db.Column(db.Integer, primary_key=True)
    fk_Post = db.Column(db.Integer, db.ForeignKey('post.postID'), nullable=False)
    fk_User = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

class CommentLike(db.Model):
    comment_like_id = db.Column(db.Integer, primary_key=True)
    fk_Comment = db.Column(db.Integer, db.ForeignKey('comment.commentID'), nullable=False)
    fk_User = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)

class PostTag(db.Model):
    post_tag_id = db.Column(db.Integer, primary_key=True)
    fk_Post = db.Column(db.Integer, db.ForeignKey('post.postID'), nullable=False)
    fk_Tag = db.Column(db.Integer, db.ForeignKey('tag.tagID'), nullable=False)
