from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session, render_template, request, redirect
from os import getenv
from app import app

def login(username,password):
    sql = "SELECT password, id, usertype FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["username"] = username
            session["usertype"] = user[2]
            return True
        else:
            return False

def user_id():
    return session.get("user_id",0)
    
def logout():
    del session["user_id"]
    del session["username"]
    del session["usertype"]
    
def register(username,password,usertype):
    hash = generate_password_hash(password)
    if len(username) < 3 or len(username) > 20 or len(password) < 6 or len(password) > 32:
        return "Käyttäjätunnuksen tulee sisältää 3-20 merkkiä ja salasanan 6-32."
    try:
        sql = "INSERT INTO users (username,password,usertype) VALUES (:username,:password,:usertype)"
        db.session.execute(sql, {"username":username,"password":hash,"usertype":usertype})
        db.session.commit()
    except:
        return "Rekisteröityminen epäonnistui. Kokeile toista käyttäjätunnusta"
    return login(username,password)
