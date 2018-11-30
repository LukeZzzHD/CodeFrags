from flask import render_template, request, Blueprint, flash
from website.models import Post, Language

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    posts = Post.query.filter_by()\
        .order_by(Post.datetime.desc())
    return render_template('home.html', title="Home", posts=posts)

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')
