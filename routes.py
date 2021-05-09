from app import app
from db import db
from flask import redirect, request, session, render_template, make_response
import base64
import users
import actions

@app.route("/")
def index():
    sql = "SELECT * FROM news WHERE visible=1 ORDER BY id DESC"
    result = db.session.execute(sql)
    news = result.fetchall()
    return render_template("news.html", news=news, topics=actions.gettopics(), amount = actions.getbookmarks(), message="")

@app.route("/news/<int:id>")
def news(id):
    sql = "SELECT * FROM news WHERE id=:id AND visible=1"
    result = db.session.execute(sql, {"id":id})
    sql2 = "SELECT * FROM comments WHERE news_id=:id AND visible=1 "
    result2 = db.session.execute(sql2, {"id":id})
    news = result.fetchall()
    comments = result2.fetchall()
    actions.addview(id)
    
    sqlcheck = "SELECT COUNT(*) FROM images WHERE news_id=:id"
    resultcheck = db.session.execute(sqlcheck, {"id":id})
    amount = resultcheck.fetchone()[0]
    if amount == 0:
        return render_template("piece.html", news=news, comments=comments, topics=actions.gettopics(), amount=actions.getbookmarks())
    
    sql3 = "SELECT data FROM images WHERE news_id=:id"
    result3 = db.session.execute(sql3, {"id":id})
    image = result3.fetchone()[0]
    image64 = base64.b64encode(image)
    return render_template("piece.html", news=news, comments=comments, image=image64.decode('utf-8'), topics=actions.gettopics(), amount=actions.getbookmarks())
    
@app.route("/mostviewed")
def mostviewed():
    sql = "SELECT * FROM news WHERE visible=1 ORDER BY views DESC"
    result = db.session.execute(sql)
    news = result.fetchall()
    return render_template("news.html", news=news, topics=actions.gettopics(), amount=actions.getbookmarks(), message="Luetuimmat uutiset:")

@app.route("/<string:topic>")
def topics(topic):
    sql = "SELECT * FROM news WHERE topic=:topic AND visible=1"
    result = db.session.execute(sql, {"topic":topic})
    news = result.fetchall()
    return render_template("news.html", news=news, topics=actions.gettopics(), topic = topic, amount=actions.getbookmarks(), message="aiheen {} uutiset:".format(topic))

@app.route("/create")
def create():
    return render_template("register.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usertype = request.form["usertype"]
        message = users.register(username,password,usertype)
        if message != True:
            return render_template("register.html", message=message)
        return redirect("/")
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect(request.referrer)
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")
            
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/result")
def result():
    search = request.args["search"]
    sql = "SELECT * FROM news WHERE (LOWER(title) LIKE LOWER(:search) OR LOWER(body) LIKE LOWER(:search) OR LOWER(topic) LIKE LOWER(:search)) AND visible=1"
    result = db.session.execute(sql,{"search":"%"+search+"%"})
    news = result.fetchall()
    return render_template("news.html", news=news, search=search, topics=actions.gettopics(),amount=actions.getbookmarks(), message="Tulokset haulle '{}':".format(search))
    
@app.route("/comment", methods=["POST"])
def comment():
    comment = request.form["comment"]
    username = session["username"]
    news_id = request.form["news_id"]
    message = actions.comment(news_id,username,comment)
    if message != True:
        return render_template("error.html", message = message)
    return redirect("/news/"+news_id)
    
@app.route("/newpiece")
def newpiece():
    return render_template("newpiece.html", topics=actions.gettopics(), amount=actions.getbookmarks())

@app.route("/publish", methods=["POST"])
def publish():
    username = session["username"]
    title = request.form["title"]
    body = request.form["body"]
    topic = request.form["topic"]
    file = request.files["file"]
    message = actions.publish(username, title, body, file, topic)
    if message != True:
        return render_template("error.html", message=message)
    elif message == False:
        return render_template("error.html",message="Virhe tapahtui. Ehkä et ole toimittaja")
    return redirect("/")
    
@app.route("/editpiece", methods=["POST"])
def editpiece():
    id = request.form["id"]
    title = request.form["title"]
    body = request.form["body"]
    topic = request.form["topic"]
    return render_template("editpiece.html", id=id, title=title, body=body, topic=topic, topics=actions.gettopics(), amount=actions.getbookmarks())

@app.route("/commitedit", methods=["POST"])
def commitedit():
    id = request.form["id"]
    title = request.form["title"]
    body = request.form["body"]
    message = actions.commitedit(id, title, body)
    if message != True:
        return render_template("error.html", message=message)
    return redirect("/news/" + id)
    
@app.route("/deletepiece", methods=["POST"])
def deletepiece():
    id = request.form["id"]
    actions.deletepiece(id)
    return redirect("/")

@app.route("/deletecomment", methods=["POST"])
def deletecomment():
    id = request.form["id"]
    news_id = request.form["news_id"]
    actions.deletecomment(id)
    return redirect(request.referrer)
    
@app.route("/swapbookmark", methods=["POST"])
def swapbookmark():
    news_id = request.form["news_id"]
    actions.swapbookmark(news_id)
    return redirect(request.referrer)

#@app.route("/viewbookmarks")
#def viewbookmarks():
    
