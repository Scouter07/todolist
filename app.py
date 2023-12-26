import helpers
import sqlite3

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

@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

@app.route("/")
def index():
    if (helpers.isloggedin() == False): # Checking if there is a user logged if not returns them to login page
        return redirect("/login")
    cursor = get_db()[1]
    tasks = cursor.execute("SELECT * FROM tasks WHERE username = ?;", (session["user_id"],)).fetchall()
    print(tasks)
    return render_template("index.html", user=session["user_id"])

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if not username or not password:
            print("Enter a valid user and password")
            return render_template("login.html")
        
        cursor = get_db()[1]
        data = cursor.execute("SELECT * FROM users WHERE user_id = ?", (username,)).fetchall()
        if len(data) != 1:
            print("Enter a valid username")
            return render_template("login.html")
        if (helpers.check_password_hash(data[0][1], password) == False):
            print("Incorrect password")
            return render_template("login.html")
        
        session["user_id"] = data[0][0]
        return redirect("/")
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    # Clears the session
    session.clear()
    
    # Closing the connection between the dataase
    get_db()[0].close()
    
    return redirect("/")
    
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        cursor = get_db()[1]
        rows = cursor.execute("SELECT * FROM users WHERE user_id = ?", (username,)).fetchall()
        if not username or rows:
            return render_template("register.html")

        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation or password != confirmation:
            return render_template("register.html")

        hashed_password = helpers.hash_password(password)
        cursor.execute("INSERT INTO users (user_id, password) VALUES (?, ?)", (username, hashed_password))
        g.db.commit()
        return redirect("/login")
    return render_template("register.html", user=session["user_id"])

@app.route("/add", methods = ["POST", "GET"])
def add():
    if (helpers.isloggedin() == False): # Checking if the 
        return redirect("/login")
    if request.method == "POST":
        name = request.form.get("tname")
        if not name:
            return render_template("add.html")
        description = request.form.get("description")
        if not description:
            description = None
        date = request.form.get("date")
        if not date:
            date = None
        time = request.form.get("time")
        if not time:
            time = None
            
        cursor = get_db()[1]
        cursor.execute("INSERT INTO tasks (name, description, date, time, username) VALUES (?,?,?,?,?)", (name, description, date, time, session["user_id"]))
        g.db.commit()
        return redirect("/")
    return render_template("add.html")