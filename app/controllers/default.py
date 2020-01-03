from flask import flash, render_template
from flask import redirect, request, url_for
from app import app, db, login_manager
from app.models.forms import LoginForm, UserRegisterForm
from app.models.forms import TaskForm
from app.models.tables import User, Task
from app.controllers.manager import Manager
from flask_login import login_user, logout_user 
from flask_login import login_required, current_user
from werkzeug.security import (generate_password_hash, 
                               check_password_hash)


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


# ---------------------------------------
#             INDEX METHODS 
#----------------------------------------
@app.route('/home')
@app.route('/index')
@app.route("/")
def index():
    return render_template('index.html')


# ---------------------------------------
#             METHODS FOR USER 
#----------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit(): 

            exists_user = User.query.all()

            for usr in exists_user[::-1]:
                if usr.username == form.username.data:
                    flash("Username already exists", 'warning')
                    return render_template(
                        'register.html', 
                        myform=form
                    )
                
                if usr.email == form.email.data:
                    flash("User email already exists", 'warning')
                    return render_template(
                        'register.html', 
                        myform=form
                    )
            
            if not (form.password.data == form.confirm_pwd.data):
                flash('Passwords do not match', 'danger')
                return render_template(
                    'register.html', 
                    myform=form
                )
            
            new_user = User(
                username=form.username.data,
                password=generate_password_hash(form.password.data),
                name=form.name.data,
                email=form.email.data
            )
            db.session.add(new_user)
            db.session.commit()
            flash('User created successfuly', 'success')
            return redirect(url_for('login'))
        if not form.validate_on_submit():
            flash('Passwords do not match', 'danger')
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
            flash(u'Invalid Login. Wrong username', 'danger') 
            return redirect('login')

        if not  check_password_hash(user.password, form.password.data):
            flash(u'Invalid Login. Wrong password.', 'danger') 
            return redirect(url_for('login'))
       
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(u'Logged in.', 'success')
            return redirect(url_for('task_doing'))
    else:
        return render_template(
            'login.html', 
            myform=form
        )

# ---------------------------------------
#     TASK: CRUD AND OTHERS METHODS
#----------------------------------------

@app.route('/task_insert', methods=['GET', 'POST'])
@login_required
def task_insert():
    
    # all_task = Task.query.all()

    '''
    This verification do not necessary because tasks are shown 
    according to the user. 
    One user will not see task created by other user
    ----------------

    for t in all_task:
        if t.task_name == request.form['taskTitleName']:
            flash(u'This task name already exists!','warning')
            return redirect(url_for('task_doing'))
    '''

    date_add = Manager().numeric_date_recover()
    new_task = Task(
        task_name=request.form['taskTitleName'],
        description=request.form['descripName'],
        start_date=date_add,
        deadline=request.form['deadlineName'],
        done_status=False,
        user_id=current_user.id
    )

    db.session.add(new_task)
    db.session.commit()

    flash('Task created successfuly', 'success')
    return redirect(url_for('task_doing'))


# ---------------------------------------
#     TASK: CRUD AND OTHERS METHODS
#----------------------------------------
@app.route('/task_doing', methods=['GET', 'POST'])
@login_required
def task_doing():

    task_form = TaskForm()   

    tasks = Task.query.filter_by(user_id=current_user.id)
    task_doing_amount = 0
    for t in tasks:
        if t.done_status == False:
            task_doing_amount += 1 

    return render_template(
        'task_doing.html', 
        tasks=tasks, 
        task_form=task_form,
        amount=task_doing_amount
    )


@app.route('/task_done', methods=['GET', 'POST'])
@login_required
def task_done():
    
    task_form = TaskForm()
    tasks = Task.query.filter_by(user_id=current_user.id)

    if request.method == "POST":
        
        if request.form['optHidden'] == 'done':
            task_done = Task.query.get(
                request.form['optDoneId']
            )
            task_done.done_status = True
            db.session.add(task_done)
            db.session.commit()

            flash('Task done successfuly', 'success')
            return render_template(
                'task_done.html', 
                tasks=tasks, 
                task_form=task_form
            )
   
    task_done_amount = 0
    for t in tasks:
        if t.done_status == True:
            task_done_amount += 1 

    return render_template(
        'task_done.html', 
        tasks=tasks, 
        task_form=task_form,
        amount=task_done_amount
    )


@app.route('/task_pre_update/<int:task_id>', 
    methods=['GET', 'POST'])
@login_required
def task_pre_update(task_id):
       
    tasks = Task.query.all()
    task2update = Task.query.get(task_id)
    return render_template(
        'task_update.html', 
        tasks=tasks, 
        t2u=task2update
    )


@app.route('/task_update/<int:task_id>', 
    methods=['GET', 'POST'])
@login_required
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

        flash('Task updated successfuly', 'success')
        
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
@login_required
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

            flash('Task deleted successfuly', 'success')

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


# ---------------------------------------
#     USER: LOGOUT METHOD
#----------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
