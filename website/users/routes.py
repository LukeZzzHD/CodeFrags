from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from website import db, bcrypt
from website.main.routes import getLikeFun, getLikeIcon
from website.models import User, Post, Language, Comment, CommentLike, PostLike
from website.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                 RequestResetForm, ResetPasswordForm, NewPostForm)
from website.users.utils import save_picture

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'secondary')
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.datetime.desc())
    resultlength = posts.count()
    return render_template('user_posts.html', posts=posts, user=user, resultlength=resultlength, getLikeIcon=getLikeIcon, getLikeUrl=getLikeUrl)

@users.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = NewPostForm()
    if form.validate_on_submit():
        lang_id = Language.query.filter_by(name=form.language.data).first().id
        post = Post(title=form.title.data, code=form.code.data, user_id=current_user.id, language_id=lang_id, description=form.description.data)
        db.session.add(post)
        db.session.commit()
        flash('You post has been created successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New', form=form)

@users.route("/user/<int:id>/delete")
@login_required
def delete_user(id):
    if current_user.email != 'admin@cfrags.com' and current_user.id != id:
        flash('You don\'t have permission to do this!', 'danger')
        return redirect(url_for('main.home'))
    user = User.query.filter_by(id=id).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    comments = Comment.query.filter_by(user_id=user.id).all()
    comment_likes = CommentLike.query.filter_by(user_id=user.id).all()
    post_likes = PostLike.query.filter_by(user_id=user.id).all()
    for post in posts:
        db.session.delete(post)
    for comment in comments:
        db.session.delete(comment)
    for comment_like in comment_likes:
        db.session.delete(comment_like)
    for post_like in post_likes:
        db.session.delete(post_like)
    db.session.delete(user)
    db.session.commit()

    flash('The user ' + user.username + ' has been deleted successfully!', 'success')
    return redirect(url_for('main.home'))

@users.route("/allusers")
def all_users():
    users = User.query.all()
    if users:
        return render_template("users.html", users=users)

    else:
        flash('There are no users registered!', 'warning')
        return redirect(url_for('main.home'))
