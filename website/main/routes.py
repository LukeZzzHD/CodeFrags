from flask import render_template, request, Blueprint
from website.models import Post

main = Blueprint('main', __name__)

posts = [
    {},
    {}
]

@main.route("/")
@main.route("/home")
def home():
    flash("You have reached our Home Page!", "success")
    return render_template('home.html', title="Home")
