import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# --------------------------HOMEPAGE------------------------- #


@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("index.html")


# --------------------------BOOKS---------------------------- #


@app.route("/books")
def books():
    books = mongo.db.books.find().sort("chronological_number")
    return render_template("books.html", books=books)


# Route for individual book page
@app.route("/books/<book_id>", methods=["GET", "POST"])
def book(book_id):
    book_id = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    
    return render_template("book_page.html", book_id=book_id)


# --------------------------ABOUT---------------------------- #


@app.route("/about")
def about():
    return render_template("about.html")


# --------------------------FAQ------------------------------ #


@app.route("/faq")
def faq():
    return render_template("faq.html")


# --------------------------SIGNUP-------------------------- #


@app.route("/signup")
def signup():
    return render_template("signup.html")


# --------------------------CONTACT------------------------- #


@app.route("/contact")
def contact():
    return render_template("contact.html")


# Don't forget to put debug in if devvelopment var
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
