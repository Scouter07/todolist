import hashlib

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