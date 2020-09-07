from datetime import datetime
from flask import current_app
from promeet import db, loginManager
from flask_login import UserMixin
from sqlalchemy.sql import expression
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), unique=True, nullable=False)
    prenom = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)
    likes = db.relationship('Like', backref='author', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    '''followers = db.relationship('Follow', backref='followed', lazy=False)
    follows = db.relationship('Follow', backref='follow', lazy=True)'''

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(20), default='')
    content = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('Like', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.date}', '{self.content}')"


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.post_id}')"


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), default='LIKE')
    content = db.Column(db.String(100), default='New noification')
    etat = db.Column(db.Boolean, server_default=expression.false(), default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.content}')"

'''
class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.follower_id}')"
'''

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def load_post(post_id):
    return Post.query.get(int(post_id))


def load_post_comments(post_id):
    return Comment.query.filter_by(post=load_post(post_id)).all()


def load_post_likes(post_id):
    return Like.query.filter_by(post=load_post(post_id)).all()


def load_user_notifications(user_id):
    return Notification.query.filter_by(user=load_user(user_id)).all()
