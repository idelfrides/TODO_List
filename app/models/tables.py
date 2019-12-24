""" Tables module """

from app import db


class User(db.Model):
    """ User model """

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(50), 
        unique=True, 
        nullable=False
    )
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Task(db.Model):
    """ Task model """

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String)
    description = db.Column(db.Text)
    start_date = db.Column(
        db.String, 
        server_default=db.func.now(),
        nullable=False
    )
    
    done_status = db.Column(db.Boolean, default=False)
    deadline = db.Column(db.String, nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        
    # ---------------------------
    task_owner = db.relationship('User', foreign_keys=user_id)

    def __init__(self, task_name, description, start_date, deadline, done_status):
        self.task_name = task_name
        self.description = description  
        self.start_date = start_date
        self.done_status = done_status
        self.deadline = deadline


    def __repr__(self):
        return '<Task %r>' % self.id

