from app import app
from db import db
from flask import redirect, request, session, render_template

def gettopics():
    sql = "SELECT topic FROM topics"
    result = db.session.execute(sql)
    topics = result.fetchall()
    return topics

def comment(news_id,username,comment):
    try:
        sql = "INSERT INTO comments (news_id, username, comment, date) VALUES (:news_id, :username, :comment, NOW())"
        db.session.execute(sql, {"news_id":news_id, "username":username, "comment":comment})
        db.session.commit()
        return True
    except:
        return False

def publish(username,usertype,title,body,topic):
    if usertype == "toimittaja":
        sql = "INSERT INTO news (title, body, reporter, date, views, topic, visible) VALUES (:title, :body, :username, NOW(), 0, :topic, 1)"
        db.session.execute(sql, {"title":title, "body":body, "username":username, "topic":topic})
        db.session.commit()
        return True;
    else:
        return False;

def addview(id):
    sql = "UPDATE news SET views = views + 1 WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True;
    
def deletepiece(id):
    sql = "UPDATE news SET visible = 0 WHERE id=:id"
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return True;
