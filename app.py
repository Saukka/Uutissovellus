from flask import Flask
from flask import redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    sql = "SELECT * FROM news ORDER BY id DESC"
    result = db.session.execute(sql)
    news = result.fetchall()
    return render_template("news.html", news=news) 

@app.route("/news/<int:id>")
def news(id):
    sql = "SELECT * FROM news WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    news = result.fetchall()
    return render_template("piece.html", news=news)
