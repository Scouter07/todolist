import hashlib
from datetime import datetime, date

from flask import redirect, render_template, session

def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()

def check_password_hash(hash_password, password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest() == hash_password

def isloggedin():
    return (session.get("user_id") is None) == False

def sort_tasks(tasks):
    pending_tasks = []
    current_tasks = []
    upcoming_tasks = []
    today = date.today()
    for task in tasks:
        task = list(task)
        if task[2] is None:
            task[2] = "-"
        if task[4] is None:
            task[4] = "-"
        if datetime.strptime(task[3], "%Y-%m-%d").date() == today:
            current_tasks.append(task)
        elif datetime.strptime(task[3], "%Y-%m-%d").date() > today:
            upcoming_tasks.append(task)
        else:
            pending_tasks.append(task)
    current_tasks.sort(key=lambda x: x[4])
    upcoming_tasks.sort(key=lambda x: (x[3], x[4]))
    return [pending_tasks, current_tasks, upcoming_tasks]
    