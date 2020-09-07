from flask import Blueprint, flash, redirect, url_for, render_template, abort, request
from flask_login import login_required, current_user

from promeet import db
from promeet.posts.utils import save_picture
from promeet.models import Post, load_user_notifications
from promeet.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/posts/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    notifications = load_user_notifications(current_user.id)
    if form.validate_on_submit():
        print(form.picture.data)
        if form.picture.data:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            picture_file = save_picture(form.picture.data)
            post.image_file = picture_file
            db.session.add(post)
            db.session.commit()
            print("OK")
        flash('Your posts has been created!', 'success')
        return redirect(url_for('main.home'))
    print("NON OK")
    return render_template('upload.html', user=current_user, title='New Post', notifications=notifications,
                           form=form, legend='New Post')


@posts.route("/posts/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', title=post.title, post=post)


@posts.route("/posts/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your posts has been updated!', 'success')
        return redirect(url_for('posts.posts', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/posts/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your posts has been deleted!', 'success')
    return redirect(url_for('main.home'))
