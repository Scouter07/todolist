import helpers
import sqlite3
from datetime import date, timedelta

from flask import Flask, redirect, render_template, request, session, g
from flask_session import Session

app = Flask(__name__)

# COnfiguring the flask session 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Using flask's g object to use the database connection for multiple threads
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("todo.db")
        g.cursor = g.db.cursor()
    return g.db, g.cursor

# Closing the connection witht he database in case of abrupt stop to the program
@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

@app.route("/", methods = ["POST", "GET"])
def index():
    if (helpers.isloggedin() == False): # Checking if there is a user logged if not returns them to login page
        return redirect("/login")
    
    # Accesing the cursor from flask's g object
    cursor = get_db()[1]
    if request.method == "POST":
        id = request.form.get("c_task")
        # Removve the given task from the database as its completed if the method is POST
        cursor.execute("DELETE from tasks WHERE id = ?", (id,))
        g.db.commit()
        pass
    
    # Gets the task for next 7 days and any task before todays date from the database
    day = date.today() + timedelta(days= 7)
    tasks = cursor.execute("SELECT * FROM tasks WHERE username = ? AND (date(date) <= date(?) OR date IS NULL)", (session["user_id"], day.strftime("%Y-%m-%d"))).fetchall()
    
    # Sorts all the tasks accordingly as the tasks bing added can be of any order
    sorted_tasks = helpers.sort_tasks(tasks)
    
    # Returning the sorted tasks
    return render_template("index.html", user=session["user_id"], pending=sorted_tasks[0], current=sorted_tasks[1], upcoming=sorted_tasks[2])

@app.route("/login", methods = ["POST", "GET"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        cursor = get_db()[1]
        data = cursor.execute("SELECT * FROM users WHERE user_id = ?", (username,)).fetchall()
        if len(data) != 1:
            error = "Could not find username in the database"
            return render_template("login.html", error=error)
        if (helpers.check_password_hash(data[0][1], password) == False):
            error = "Incorrect password"
            return render_template("login.html", error=error)
        
        session["user_id"] = data[0][0]
        return redirect("/")
    else:
        return render_template("login.html", error=error)
    
@app.route("/logout")
def logout():
    # Clears the session
    session.clear()
    
    # Closing the connection between the dataase
    get_db()[0].close()
    
    return redirect("/")
    
@app.route("/register", methods = ["POST", "GET"])
def register():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        if len(username) > 20:
            error = "Username can't be more than 20 characters."
            return render_template("register.html", error=error)
            
        cursor = get_db()[1]
        rows = cursor.execute("SELECT * FROM users WHERE user_id = ?", (username,)).fetchall()
        if rows:
            error = "Username already exists"
            return render_template("register.html", error=error)

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hashed_password = helpers.hash_password(password)
        cursor.execute("INSERT INTO users (user_id, password) VALUES (?, ?)", (username, hashed_password))
        g.db.commit()
        return redirect("/login")
    return render_template("register.html", error=error)

@app.route("/add", methods = ["POST", "GET"])
def add():
    if (helpers.isloggedin() == False): # Checking if the 
        return redirect("/login")
    if request.method == "POST":
        name = request.form.get("tname")
        date = request.form.get("date")
        description = request.form.get("description")
        if not description:
            description = None
        time = request.form.get("time")
        if not time:
            time = None
            
        cursor = get_db()[1]
        cursor.execute("INSERT INTO tasks (name, description, date, time, username) VALUES (?,?,?,?,?)", (name, description, date, time, session["user_id"]))
        g.db.commit()
        return redirect("/")
    return render_template("add.html", user=session["user_id"])

@app.route("/changepassword", methods = ["POST", "GET"])
def change_password():
    error = None
    if request.method == "POST":
        password = request.form.get("password")
        cursor = get_db()[1]
        row = cursor.execute("SELECT * FROM users WHERE user_id = ?", (session["user_id"],)).fetchone()
        if not helpers.check_password_hash(row[1], password):
            error = "Incorrect Password"
            return render_template("changepassword.html", error=error)
        newpassword = request.form.get("newpassword")
        confirmation = request.form.get("confirmation")
        if password == newpassword:
            error = "New password can't be equal to the old password."
            return render_template("changepassword.html", error=error)
        if newpassword != confirmation:
            error = "Confirmation should be equal to the new password."
            return render_template("changepassword.html", error=error)
        cursor.execute(
            "UPDATE users SET password = ? WHERE user_id = ?",
            (helpers.hash_password(newpassword),
            session["user_id"])
        )
        g.db.commit()
        return redirect("/")
    return render_template("changepassword.html",error=error)