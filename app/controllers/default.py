from flask import render_template, redirect, request
from app import app, db
from app.models.forms import LoginForm, RegisterForm
from app.models.forms import TaskForm
from app.models.tables import User, Task
from app.controllers.manager import Manager


@app.route('/home')
@app.route('/index')
@app.route("/")
def index():
    return render_template('index.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)

        if not (form.password.data == form.confirm_pwd.data):
            print('\n passwords do not match\n\n')
            return render_template('register.html', myform=form)
        
        new_user = User(
            username=form.username.data,
            password=form.password.data,
            name=form.name.data,
            email=form.email.data
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect('login')
       
    if not form.validate_on_submit():
        print(form.errors)

    return render_template('register.html', myform=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)

        # CKECK IS EACH USER EXISTS

        return redirect('task_registered')
       
    if not form.validate_on_submit():
        print(form.errors)

    return render_template('login.html', myform=form)


@app.route('/user/create/<info>')
@app.route('/user/create', methods=['GET'], 
    defaults={'info': None}
)
def create_user(info):
    usr = User(
        username='cafe',
        password='14657',
        name='escolastica',
        email='cafe@teste.com'
    )
    db.session.add(usr)
    db.session.commit()
    return 'OK'
    

@app.route('/read/<id>')
@app.route('/read', methods=['GET'], 
    defaults={"id":None})
def read(id):
    if id:
       # usr_h = User.query.get(id)
        #name = usr_h.name
        usr = User.query.filter_by(id=id).all()

    if not id:
        usr = User.query.all()

    print(usr)
    return 'OK'


@app.route('/delete/<id>')
@app.route('/delete', methods=['GET'],
    defaults={"id":None})
def delete_user(id):
    if id:
        usr = User.query.filter_by(name='cafe2').all()
        #name = usr_h.name
        # usr = User.query.filter_by(id=id).all()

    if not id:
        usr = User.query.all()

    print(usr)
    db.session.delete(usr)
    db.session.commit()
    return 'OK'


# ---------------------------------------
#                 TASK 
#----------------------------------------
@app.route('/task/create', methods=['GET', 'POST'])

def create_task():    
    task = Task(
        task_name='study python',
        description='description',
        start_date=db.func.now(),
        deadline=None,
        done_status =False
    )
    db.session.add(task)
    db.session.commit()
    return 'OK'


@app.route('/task_insert', methods=['GET', 'POST'])
def task_insert_all():
    print('\n\n EU SOU TASK INSERT \n\n')
    if request.method == 'POST':
        task_data = {}
        # task_data['title'] = request.POST.get("taskTitleName")
        task_data['desc'] = request.POST.get("descripName")
        task_data['deadline'] = request.POST.get("deadlineName")
    
        task = Task(
            task_name=request.POST.get("taskTitleName"),
            description=task_data['desc'],
            start_date=db.func.date(),
            deadline=task_data['deadline'],
            done_status=False
        )
        db.session.add(task)
        db.session.commit()
        print('\n\n TASK INSERED SUCCESSFULLY\n')

        return redirect('task_doing')
 

@app.route('/task/read/<id>')
@app.route('/task/read', methods=['GET'], 
    defaults={"id":None})
def read_task(id):
    if id:
       # usr_h = User.query.get(id)
        #name = usr_h.name
        task = Task.query.filter_by(id=id).all()
    if not id:
        task = Task.query.all()

    print(task)
    return 'OK'


@app.route('/task/update/<id>')
@app.route('/task/update', methods=['GET', 'POST'],
    defaults={"id":None}
)
def update_task(id):
    if id:
        task2update = Task.query.get(id)
        task2update.done_status = True
        db.session.commit()

        task_form = TaskForm()
        task = Task.query.all()

    return render_template(
        'task_doing.html', 
        task=task, 
        task_form=task_form
    )


@app.route('/task_dalete/<id>')
@app.route('/delete_task', methods=['GET'],
    defaults={"id":None}
)
def task_dalete(id):
    if id:
        # task = Task.query.filter_by(id).all()
        task = Task.query.get(id)
       
        #name = usr_h.name
        # usr = User.query.filter_by(id=id).all()
        print('\n\n QUERY RESULT: ', task)

    if id == None:
        print('EU SOU NONE')
        task = Task.query.all()

    print(task.task_name, task.user_id, task.description)
    db.session.delete(task)
    db.session.commit()

    task_form = TaskForm()
    task = Task.query.all()
    return render_template(
        'task_doing.html', 
        task=task, 
        task_form=task_form
    )


@app.route('/task_registered', methods=['GET', 'POST'])
def task_registered():
    if request.method == "POST":
        
        task_data = {}
        task_data['title'] = request.form['taskTitleName']
        task_data['desc'] = request.form['descripName']
        task_data['deadline'] = request.form['deadlineName']
        
        date_add = Manager().numeric_date_recover()

        task = Task(
            task_name=request.form['taskTitleName'],
            description=request.form['descripName'],
            start_date=date_add,
            deadline=request.form['deadlineName'],
            done_status=False
        )

        print('\n\n DATA FROM MODAL {}\ntask: {}\ndate add {}'
            .format(task_data, task, date_add)
        )
        db.session.add(task)
        db.session.commit()
        print('\n\n TASK INSERED SUCCESSFULLY\n')

        return redirect('task_doing')

    task_form = TaskForm()
    task = Task.query.all()

    return render_template('manage_task.html', task=task, task_form=task_form)


@app.route('/task_doing', methods=['GET', 'POST'])
def task_doing():
    if request.method == "POST":
        if request.form['optHidden'] == 'done':
            return redirect(
                '/task/update/',
                  request.form['optDoneId']
            )

        if request.form['optHidden'] == 'remove':
    
            task2delete = Task.query.get(
                request.form['optRemoveId']
            )

            db.session.delete(task2delete)
            db.session.commit()
            

    task_form = TaskForm()
    task = Task.query.all()
    return render_template(
        'task_doing.html', 
        task=task, 
        task_form=task_form
    )
    


@app.route('/task_done')
def task_done():
    task_form = TaskForm()
    task = Task.query.all()

    return render_template('task_done.html', task=task, task_form=task_form)



