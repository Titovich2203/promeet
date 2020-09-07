from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from promeet.models import Like, load_post


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Post Picture', validators=[DataRequired(), FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Upload')


class CommentForm(FlaskForm):
    content = StringField('Write your comment', validators=[DataRequired()])
    post = StringField('', validators=[DataRequired()])
    submit = SubmitField('Post')


class LikeForm(FlaskForm):
    post = StringField('', validators=[DataRequired()])
    submit = SubmitField('Like')
'''
    def validate(self, post):
        like = Like.query.filter_by(post=load_post(post.data), author=current_user).first()
        if like:
            raise ValidationError("DEJA LIKE")
'''