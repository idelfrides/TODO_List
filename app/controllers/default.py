from flask import flash, render_template, redirect, request
from app import app, db
from app.models.forms import LoginForm, RegisterForm
from app.models.forms import TaskForm
from app.models.tables import User, Task
from app.controllers.manager import Manager
from flask_login import login_user


# ---------------------------------------
#             INDEX METHODS 
#----------------------------------------
@app.route('/home')
@app.route('/index')
@app.route("/")
def index():
    return render_template('index.html')


# ---------------------------------------
#              METHODS FOR USER 
#----------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':

        if form.validate_on_submit():
            if not (form.password.data == form.confirm_pwd.data):
                flash('Passwords do not match')
                return render_template(
                    'register.html', 
                    myform=form
                )        
            new_user = User(
                username=form.username.data,
                password=form.password.data,
                name=form.name.data,
                email=form.email.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfuly')

            return redirect('login')
        if not form.validate_on_submit():
            print(form.errors)
            return render_template(
                'register.html', 
                myform=form
            )
    else:
        return render_template(
            'register.html', 
            myform=form
        )
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
  
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if not user:
            flash('Invalid Login. Wrong username') 
            return redirect('login')

        if user.password != form.password.data:
            flash('Invalid Login. Wrong password.') 
            return redirect('login')
       
        if user.password == form.password.data:
            flash('Logged in.')
            # login_user(user)
            return redirect('task_doing')
    
    if not form.validate_on_submit():       
        return render_template(
            'login.html', 
            myform=form
        )

# ---------------------------------------
#     TASK: CRUD AND OTHERS METHODS
#----------------------------------------

@app.route('/task_insert', methods=['GET', 'POST'])
def task_insert(): 
     
    date_add = Manager().numeric_date_recover()

    new_task = Task(
        task_name=request.form['taskTitleName'],
        description=request.form['descripName'],
        start_date=date_add,
        deadline=request.form['deadlineName'],
        done_status=False
    )

    db.session.add(new_task)
    db.session.commit()

    flash('Task created successfuly')
    return redirect('task_doing')


@app.route('/task_pre_update/<int:task_id>', methods=['GET', 'POST'])
def task_pre_update(task_id):
       
    tasks = Task.query.all()
    task2update = Task.query.get(task_id)
    return render_template(
        'task_update.html', 
        tasks=tasks, 
        t2u=task2update
    )


@app.route('/task_update/<int:task_id>', methods=['GET', 'POST'])
def task_update(task_id):
    task_form = TaskForm()   

    if request.method == "POST":        
        task2update = Task.query.get(task_id)

        date_add = Manager().numeric_date_recover()
        
        task2update.task_name=request.form['taskTitleName']
        task2update.description=request.form['descripName']
        task2update.start_date=date_add
        task2update.deadline=request.form['deadlineName']
        task2update.done_status=False
        
        db.session.add(task2update)
        db.session.commit()

        flash('Task updated successfuly')
        
        tasks = Task.query.all()
        return render_template(
            'task_doing.html', 
            tasks=tasks, 
            task_form=task_form
        )
    else:
        tasks = Task.query.all()
        return render_template(
            'task_doing.html', 
            tasks=tasks, 
            task_form=task_form
        )


@app.route('/task_delete', methods=['GET', 'POST'])
def task_delete():
    task_form = TaskForm()
    tasks = Task.query.all()

    if request.method == 'POST':
        if request.form['optHidden'] == 'remove':
            task2delete = Task.query.get(
                request.form['optRemoveId']
            )

            db.session.delete(task2delete)
            db.session.commit()

            flash('Task deleted successfuly')

            tasks = Task.query.all()
            return render_template(
                'task_doing.html', 
                tasks=tasks, 
                task_form=task_form
            )
  
    return render_template(
        'task_doing.html', 
        tasks=tasks, 
        task_form=task_form
    )


@app.route('/task_doing', methods=['GET', 'POST'])
def task_doing():

    task_form = TaskForm()   

    tasks = Task.query.all()
    return render_template(
        'task_doing.html', 
        tasks=tasks, 
        task_form=task_form
    )


@app.route('/task_done', methods=['GET', 'POST'])
def task_done():
    
    task_form = TaskForm()
    tasks = Task.query.all()

    if request.method == "POST":
        
        if request.form['optHidden'] == 'done':
            task_done = Task.query.get(
                request.form['optDoneId']
            )
            task_done.done_status = True
            db.session.add(task_done)
            db.session.commit()

            flash('Task done successfuly')
            return render_template(
                'task_done.html', 
                tasks=tasks, 
                task_form=task_form
            )
    return render_template(
        'task_done.html', 
        tasks=tasks, 
        task_form=task_form
    )





