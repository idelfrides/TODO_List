# TODO_List


This project is about an approach  of **todoist** project manager app.
This project apply the **CLEAN CODE filosophy and SOLID principles**  and software design pattern **MVC - Model-View-Controller**. 


## Executing this app in your computer
To execute and test this app locally, you need to make some few steps bellow.


### STEP 1: Cloning this repository

On your laptop or desktop clone this repository with command 

     git clone https://github.com/idelfrides/TODO_List.git 


Then, open your shell/terminal and go to the project folder **TODO_List**  with **cd** shell commend.

### STEP 2: Creating a virtualenv 

In project root create a virtualenv for your project like bellow.

     virtualenv -p python3.7 ENV 


### STEP 3: Ativate the virtualenv 

To active virtualenv created  type command  like bellow.

     source ENV/bin/activate
     
If you are using **FISH** - Friendly Interative Shell, type this one.

     source ENV/bin/activate.fish
     

### STEP 4: Install all flask dependency

To run app you need to install apckages used in this project. To do that execute the follwing  command.

     pip install -r ./requirement.text


### STEP 5: Run the app

If everything in previous steps complete successfuly, now you are able to run this app. Execute  the follwing  command to do that.

     python todo_list_run.py runserver
     

### STEP 6: Create a user

Creat your user to login into app and test it.  Copy the localhost and paste it on your url of browser, so you are free to test all components you see on your page. Do not forget, that, to log in and create some tasks you gonna need to create your own user acount on page **Cadastro/Register**. 

    http://127.0.0.1:5000/
     

Go ahead and enjoy.
 







