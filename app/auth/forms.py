from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User

class SignupForm(FlaskForm):
    email = StringField("Enter Your Email Address", render_kw={'placeholder': 'Email'},
                        validators=[DataRequired(), Email()])
    username = StringField("Username", render_kw={"placeholder": "username"}, validators=[DataRequired()])
    password = PasswordField("Password", render_kw={"placeholder": "password"},
                             validators=[DataRequired(), EqualTo('confirm_password', message="Passwords Must Match")])
    confirm_password = PasswordField("Confirm Password", render_kw={"placeholder": "Confirm password"},
                                     validators=[DataRequired()])
    signupbtn = SubmitField("Sign Up")
    
    # verify log in details
    def validate_email(self, data_field):
        if User.query.filter_by(email= data_field.data).first():
            raise ValidationError("Email Already Registered.")
        
    def validate_username(self, data_field):
        if User.query.filter_by(username= data_field.data).first():
            raise ValidationError("Username Taken. Try Another one.")


class LoginForm(FlaskForm):
    username = StringField("Username", render_kw={"placeholder": "Username"}, validators=[DataRequired()])
    password = PasswordField("Password", render_kw={"placeholder": "Password"}, validators=[DataRequired()])
    rememberMe = BooleanField("RememberMe")
    loginbtn = SubmitField("Login")

class SubscribeForm(FlaskForm):
    email = StringField("Enter Your Email Address", render_kw={'placeholder': 'Email'},
                        validators=[DataRequired(), Email()])
    subscribebtn = SubmitField("Subscribe")