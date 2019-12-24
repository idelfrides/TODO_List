from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import TextField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(
        'username', 
        validators=[DataRequired()]
    )
    password = PasswordField(
        'password', 
        validators=[DataRequired()]
    )
    remember_me = BooleanField('remember')


class TaskForm(FlaskForm):
    
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

