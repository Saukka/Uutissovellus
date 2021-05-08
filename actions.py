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
        sql = "INSERT INTO comments (news_id, username, comment, date, visible) VALUES (:news_id, :username, :comment, NOW(), 1)"
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
    username = session["username"]
    sql = "UPDATE news SET visible = 0 WHERE id=:id AND reporter=:username"
    db.session.execute(sql, {"id":id, "username":username})
    db.session.commit()
    return True;

def deletecomment(id, news_id):
    sqlcheck = "SELECT reporter FROM news WHERE id=:news_id"
    result = db.session.execute(sqlcheck, {"news_id":news_id})
    reporter = result.fetchone()[0]
    
    sqlcheck2 = "SELECT username FROM comments WHERE id=:id"
    result2 = db.session.execute(sqlcheck2, {"id":id})
    commenter = result2.fetchone()[0]
    
    username = session["username"]
    if reporter == username or commenter == username:
        sql = "UPDATE comments SET visible = 0 WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True;
    return False;

def swapbookmark(news_id):
    username = session["username"]
    sql = "SELECT COUNT(*) FROM bookmarks where username=:username AND news_id=:news_id"
    result = db.session.execute(sql, {"username":username, "news_id":news_id})
    amount = result.fetchone()[0]
    print(amount)
    if amount == 0:
        sqlinsert = "INSERT INTO bookmarks (username, news_id, visible) VALUES (:username, :news_id, 1)"
        db.session.execute(sqlinsert, {"username":username, "news_id":news_id})
        db.session.commit()
        return True;
    elif amount == 1:
        sqlset = "UPDATE bookmarks SET visible = -1 * visible WHERE username=:username AND news_id=:news_id"
        db.session.execute(sqlset, {"username":username, "news_id":news_id})
        db.session.commit()
        return True;
    return False;
