from flask import render_template, request, Blueprint, flash, send_from_directory, redirect, url_for
from website.models import Post, Language, User, PostLike, CommentLike
from flask_login import current_user
from website import db

main = Blueprint('main', __name__)

def getLikeIcon(post):
        liked = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first()
        if liked:
            return 'favorite'
        return 'favorite_border'

def getLikeUrl(post):
    liked = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if liked:
        return 'posts.unlike'
    return 'posts.like'


def getCommentLikeIcon(comment):
        liked = CommentLike.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
        if liked:
            return 'favorite'
        return 'favorite_border'

def getCommentLikeUrl(comment):
    liked = CommentLike.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
    if liked:
        return 'posts.unlike_comment'
    return 'posts.like_comment'

@main.route("/")
@main.route("/home", methods=['GET', 'POST'])
def home():
    posts = Post.query.filter_by()\
        .order_by(Post.datetime.desc())
    usercount = User.query.count()
    postcount = Post.query.count()

    return render_template('home.html', title="Home", posts=posts, usercount=usercount, postcount=postcount, getLikeIcon=getLikeIcon, getLikeUrl=getLikeUrl, resultlength=postcount)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')

@main.route('/help')
def help():
    return send_from_directory('static', 'Benutzeranleitung.pdf')
