from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from website import db
from website.models import Post, Language
from website.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, code=form.code.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:id>")
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/post/<int:id>/update", methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.code = form.code.data
        post.description = form.description.data
        post.language = Language.query.filter_by(name=form.language.data).first()
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.code.data = post.code
        form.description.data = post.description
        form.language.data = Language.query.get_or_404(post.language_id).name
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:id>/delete", methods=['POST'])
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
