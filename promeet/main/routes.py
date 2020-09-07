from flask import Blueprint, redirect, url_for, flash, render_template, request
from promeet.models import User, Post, Comment, load_post, load_post_comments, Like, load_post_likes, \
    load_user_notifications, Notification
from flask_login import current_user, login_user, logout_user, login_required
from promeet.main.forms import LoginForm, RegistrationForm
from promeet import bcrypt, db
from promeet.posts.forms import CommentForm, LikeForm

main = Blueprint('main', __name__)


# @main.route("/home")

@main.route("/", methods=['GET', 'POST'])
@main.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You have been logged in!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='CONNEXION', form=form)
    # return render_template('login.html', title='CONNEXION')


@main.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(nom=form.nom.data, prenom=form.prenom.data, username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account have been created ! Now log in', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)


@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    users = User.query.all()
    posts = Post.query.order_by(Post.date.desc()).all()
    notifications = load_user_notifications(current_user.id)
    form = CommentForm()
    form2 = LikeForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=load_post(form.post.data))
        db.session.add(comment)
        db.session.commit()
        notif = Notification(content=current_user.prenom+" a commenté votre post", user=load_post(form.post.data).author, type="COMMENT")
        db.session.add(notif)
        db.session.commit()
        form.content.data = ""
        return redirect(url_for('main.home'))
    if form2.validate_on_submit():
        like = Like(post=load_post(form.post.data), author=current_user)
        db.session.add(like)
        db.session.commit()
        notif = Notification(content=current_user.prenom+" a aimé votre post", user=load_post(form2.post.data).author, type="LIKE")
        db.session.add(notif)
        db.session.commit()
        return redirect(url_for('main.home'))
    #print(posts)
    # print(users)
    return render_template('home.html', title='HOME', formComment=form, formLike=form2, user=current_user, notifications=notifications,
                           posts=posts, utilsateurs=users, loadComments=load_post_comments, loadLikes=load_post_likes)


@main.route("/logout", )
def logout():
    logout_user()
    return redirect(url_for('main.login'))
