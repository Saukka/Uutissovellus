from app import app
from db import db
from flask import redirect, request, session, render_template
import users
import actions

@app.route("/")
def index():
    sql = "SELECT * FROM news WHERE visible=1 ORDER BY id DESC"
    result = db.session.execute(sql)
    news = result.fetchall()
    return render_template("news.html", news=news, topics=actions.gettopics())

@app.route("/news/<int:id>")
def news(id):
    sql = "SELECT * FROM news WHERE id=:id AND visible=1"
    result = db.session.execute(sql, {"id":id})
    sql2 = "SELECT * FROM comments WHERE news_id=:id AND visible=1 "
    result2 = db.session.execute(sql2, {"id":id})
    news = result.fetchall()
    comments = result2.fetchall()
    actions.addview(id)
    return render_template("piece.html", news=news, comments=comments,topics=actions.gettopics())

@app.route("/mostviewed")
def mostviewed():
    sql = "SELECT * FROM news WHERE visible=1 ORDER BY views DESC"
    result = db.session.execute(sql)
    news = result.fetchall()
    return render_template("mostviewed.html", news=news, topics=actions.gettopics())

@app.route("/<string:topic>")
def topics(topic):
    sql = "SELECT * FROM news WHERE topic=:topic AND visible=1"
    result = db.session.execute(sql, {"topic":topic})
    news = result.fetchall()
    return render_template("topic.html", news=news, topics=actions.gettopics(), topic = topic)

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
        if users.register(username,password,usertype):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut. Kokeile toista käyttäjätunnusta.")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
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
    return render_template("result.html", news=news, search=search, topics=actions.gettopics())
    
@app.route("/comment", methods=["POST"])
def comment():
    comment = request.form["comment"]
    username = session["username"]
    news_id = request.form["news_id"]
    actions.comment(news_id,username,comment)
    return redirect("/news/"+news_id)
    
@app.route("/newpiece")
def newpiece():
    return render_template("newpiece.html", topics=actions.gettopics())

@app.route("/publish", methods=["POST"])
def publish():
    username = session["username"]
    usertype = session["usertype"]
    title = request.form["title"]
    body = request.form["body"]
    topic = request.form["topic"]
    if actions.publish(username, usertype, title, body, topic):
        return redirect("/")
    else:
        return render_template("error.html",message="Virhe tapahtui. Ehkä et ole toimittaja")
    

@app.route("/deletepiece", methods=["POST"])
def deletepiece():
    id = request.form["id"]
    actions.deletepiece(id)
    return redirect("/")

@app.route("/deletecomment", methods=["POST"])
def deletecomment():
    id = request.form["id"]
    actions.deletecomment(id)
    return redirect(request.referrer)
    

