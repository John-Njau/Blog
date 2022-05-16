from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired

from ..models import User

class BlogForm(FlaskForm):
    title= StringField('Title', validators=[DataRequired()])
    blog = TextAreaField(validators=[DataRequired()])
    submit =SubmitField("Post Blog")

class CommentForm(FlaskForm):
    commentbody = TextAreaField("Comment", validators=[DataRequired()])
    postbtn = SubmitField("Post")
    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Bio', validators=[DataRequired()])
    submit = SubmitField('Save')