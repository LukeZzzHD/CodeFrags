from flask import render_template, request, Blueprint, flash
from website.models import Post

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    #flash("You have reached our Home Page!", "success")
    #flash("Watch out!", "warning")
    #flash("That's fatal", "danger")
    posts = [
        {
            user_id : 1,
            title : "Title",
            code : "<html>",
            description: "A html tag"
            
        }
    ]
    return render_template('home.html', title="Home")

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/contact")
def contact():
    return render_template('contact.html', title='Contact')
