from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from website.main.routes import getLikeUrl, getLikeIcon
from website import db
from website.models import Post, Language, Comment, PostLike
from website.posts.forms import PostForm, CommentForm

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


@posts.route("/post/<int:id>", methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.comment.data, user_id=current_user.id, post_id=post.id)
            print(comment)
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been created!', 'success')

            return redirect(url_for('main.home'))
        else:
            flash('Login to write a comment!', 'primary')
            return redirect(url_for('users.login'))

    for error in form.errors:
        flash(error)

    return render_template('post.html', title=post.title, post=post, form=form)


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

@posts.route("/search", methods=['GET', 'POST'])
def search():

    q = request.args.get('q')
    if q.strip() != "":
        flash('You searched: ' + q, 'primary')
        posts = Post.query.filter(Post.title.like("%" + q.replace(" ", "%%") + "%")).all()

        return render_template('results.html', posts=posts, getLikeUrl=getLikeUrl, getLikeIcon=getLikeIcon)

    return redirect(url_for('main.home'))


@posts.route("/post/<int:id>/like")
@login_required
def like(id):
    post = Post.query.get_or_404(id)
    isliked = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if not isliked:
        like = PostLike(user_id=current_user.id, post_id=post.id)
        db.session.add(like)
        db.session.commit()
        flash('Post was liked', 'success')

    return redirect(url_for('main.home'))

@posts.route("/post/<int:id>/unlike")
@login_required
def unlike(id):
    post = Post.query.get_or_404(id)
    isliked = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    if  isliked:
        db.session.delete(isliked)
        db.session.commit()
        flash('Post was unliked', 'secondary')

    return redirect(url_for('main.home'))
