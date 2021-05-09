from app import app
from db import db
from flask import redirect, request, session, render_template

def gettopics():
    sql = "SELECT topic FROM topics"
    result = db.session.execute(sql)
    topics = result.fetchall()
    return topics
    
def isbookmarked(id):
    if not session:
        return False;
    username = session["username"]
    sql = "SELECT COUNT(*) FROM bookmarks WHERE news_id=:id AND username=:username AND visible = 1"
    result = db.session.execute(sql, {"id":id, "username":username})
    amount = amount = result.fetchone()[0]
    if amount == 0:
        return False;
    return True;

def getbookmarks():
    if not session:
        return 0
    
    username = session["username"]
    sql = "SELECT COUNT(*) FROM bookmarks WHERE username=:username AND visible = 1"
    result = db.session.execute(sql, {"username":username})
    amount = result.fetchone()[0]
    return amount
    
def comment(news_id,username,comment):
    if (len(comment) == 0):
        return "Et voi lähettää tyhjää kommenttia."
    try:
        sql = "INSERT INTO comments (news_id, username, comment, date, visible) VALUES (:news_id, :username, :comment, NOW(), 1)"
        db.session.execute(sql, {"news_id":news_id, "username":username, "comment":comment})
        db.session.commit()
        return True
    except:
        return "Virhe tapahtui."

def publish(username, title, body, file, topic):
    if (len(title) < 10 or len(body) < 10 or len(title) > 150 or len(body) > 5000):
        return "Julkaiseminen epäonnistui. Otsikon tulee sisältää 10-150 merkkiä ja tekstin 10-5000. Otsikon pituus oli " + str(len(title)) + ", tekstin pituus " + str(len(body)) + ".";
    
    if file:
        name = file.filename
        if not name.endswith(".jpg"):
            return "Tiedoston pitää olla jpg-tiedosto."
        data = file.read()
        if len(data) > 100*1024:
            return "Tiedosto on liian suuri."
    
    usertype = session["usertype"]
    if usertype == "toimittaja":
        sql = "INSERT INTO news (title, body, reporter, date, views, topic, visible) VALUES (:title, :body, :username, NOW(), 0, :topic, 1)"
        db.session.execute(sql, {"title":title, "body":body, "username":username, "topic":topic})
        db.session.commit()
        
        if file:
            sqlid = "SELECT MAX(id) FROM news"
            result = db.session.execute(sqlid)
            amount = result.fetchone()[0]
        
            sqlimage = "INSERT INTO images (name, news_id, data) VALUES (:name, :amount, :data)"
            db.session.execute(sqlimage, {"name":name, "amount":amount, "data":data})
            db.session.commit()
        return True;
    else:
        return False;

def commitedit(id, title, body):
    username = session["username"]
    if (len(title) < 10 or len(body) < 10 or len(title) > 150 or len(body) > 5000):
        return "Muokkaaminen epäonnistui. Otsikon tulee sisältää 10-150 merkkiä ja tekstin 10-5000. Otsikon pituus oli " + str(len(title)) + ", tekstin pituus " + str(len(body)) + ".";
    sql = "UPDATE news SET title = :title, body = :body WHERE id=:id AND reporter=:username"
    db.session.execute(sql, {"title":title, "body":body, "id":id, "username":username})
    db.session.commit()
    return True;

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

def deletecomment(id):
    username = session["username"]
    sql = "UPDATE comments SET visible = 0 WHERE id=:id AND username=:username"
    db.session.execute(sql, {"id":id, "username":username})
    db.session.commit()
    return True;

def swapbookmark(news_id):
    username = session["username"]
    sql = "SELECT COUNT(*) FROM bookmarks where username=:username AND news_id=:news_id"
    result = db.session.execute(sql, {"username":username, "news_id":news_id})
    amount = result.fetchone()[0]
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
