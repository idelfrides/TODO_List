from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import TextField, validators
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """ Flash Form for user login  """
    username = StringField(
        'username', 
        validators=[DataRequired()]
    )
    password = PasswordField(
        'password', 
        validators=[DataRequired()]
    )
    remember_me = BooleanField('remember')


class UserRegisterForm(FlaskForm):
    """ Flash Form for user registration """
    name = StringField(
        'name',
        validators=[DataRequired()]
    )
    email = StringField(
        'emial',
        [validators.InputRequired(),  
        validators.Length(min=6, max=120),
        validators.Email()] 
    )
    username = StringField(
        'username', 
        [validators.Length(min=3, max=20), 
        validators.DataRequired()]
    )
    password = PasswordField(
        'password', 
        validators=[DataRequired()]
    )
    confirm_pwd = PasswordField(
        'confirme pwd',
        validators=[DataRequired()]
    )


class TaskForm(FlaskForm):
    """ Flash Form for tasks """

    taskname = StringField(
        'taskname', 
        validators=[DataRequired()]
    )
    
    description = TextField(
        'description', 
        validators=[DataRequired()]
    )
    
    deadline = StringField(
        'deadline'
    )

