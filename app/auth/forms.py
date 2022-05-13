from flask_wtf import *
from wtforms import *


class SignupForm(FlaskForm):
    email = StringField("Enter Your Email Address")

