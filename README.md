# todolist
#### Video Demo:  <URL https://www.youtube.com/watch?v=hfiXuAx8-54>
#### Description:
This is simple todo list that I have made with the help of flask framework in python, sqlite and html, css, js.
In the project a user can sign uo then sign into the site to maintain their todo list. All the tasks are sorted into pending current and upcoming tasks.
The user can then remove tasks once they are done and can add tasks accordingly.
There is also a feature for user to change their password.

App.py
This fill contains all the routing of the web pages and provides logic to the website. It does everything fromm signing up to logging in to website. It maintains the adding of tasks and sorts these function and displays is into html files as well. THis is the main app file that is needed to run project with flask run.

helpers.py
This file contains other helper function that were neccessary to imbed proper logic into the App.py file. This file contains functions such as islogged in, sort tasks, and converting passwords into hash and checking the psswords.

templates/
this folders contains all the templates that were displayed to the website from index.html to register.html, all these html files also contain jinja init to display the data provided to html pages accordingly.

static/
this folder contains all the static files such as images, css file, etc. It contains the favicon of the website and also img of the offcanvas in the website.

todo.db
this is the database that contains tables neccessary for the project it contains two tables users, tasks. Users is where user and password are stored and tasks is where all the data of the task and its unique id and the user it belongs to is stored.

requirements.txt
It is a text file that contians all the libraries neccesary to run the web app
