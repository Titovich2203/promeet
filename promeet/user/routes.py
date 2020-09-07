from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user

from promeet import db
from promeet.main.forms import UpdateAccountPictureForm
from promeet.main.utils import save_picture
from promeet.models import User, Post, load_post_likes, load_post_comments, load_post, Comment, Like, \
    load_user_notifications, Notification
from promeet.posts.forms import CommentForm, LikeForm

users = Blueprint('users', __name__)


@users.route("/account", methods=['GET', 'POST'])
def account():
    notifications = load_user_notifications(current_user.id)
    form = UpdateAccountPictureForm()
    form2 = CommentForm()
    form3 = LikeForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            db.session.commit()
            return redirect(url_for('users.account'))
    if form2.validate_on_submit():
        comment = Comment(content=form2.content.data, author=current_user, post=load_post(form2.post.data))
        db.session.add(comment)
        db.session.commit()
        notif = Notification(content=current_user.prenom+" a commenté votre post", user=load_post(form2.post.data).author, type="COMMENT")
        db.session.add(notif)
        db.session.commit()
        form2.content.data = ""
        return redirect(url_for('users.account'))
    if form3.validate_on_submit():
        print(current_user)
        like = Like(post=load_post(form3.post.data), author=current_user)
        db.session.add(like)
        db.session.commit()
        notif = Notification(content=current_user.prenom+" a aimé votre post", user=load_post(form3.post.data).author, type="LIKE")
        db.session.add(notif)
        db.session.commit()
        return redirect(url_for('users.account'))
    posts = Post.query.filter_by(author=current_user).order_by(Post.date.desc()).all()
    return render_template('profil.html', title="COMPTE", loadLikes=load_post_likes, form=form, formComment=form2, notifications=notifications,
                           formLike=form3, user=current_user, posts=posts, utilsateurs=User.query.all(),  loadComments=load_post_comments)


@users.route("/explore")
def explore():
    notifications = load_user_notifications(current_user.id)
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('explore.html', title="EXPLORE", loadLikes=load_post_likes, user=current_user, notifications=notifications,
                           posts=posts, utilsateurs=User.query.all())


@users.route("/stories")
def stories():
    notifications = load_user_notifications(current_user.id)
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('stories.html', title="STORIES", user=current_user, notifications=notifications, posts=posts)


@users.route("/notifications")
def notifications():
    notifications = load_user_notifications(current_user.id)
    return render_template('notifications.html', title="NOTIFICATIONS", user=current_user, notifications=notifications)
