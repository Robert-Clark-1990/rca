import os
from flask import (
    Flask, flash, render_template, abort,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from flask_mail import Mail, Message

from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import mail_username, mail_password
from functools import wraps

if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MAIL_SERVER"] = "server191.web-hosting.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = mail_username
app.config["MAIL_PASSWORD"] = mail_password
app.config["UPLOAD_EXTENSIONS"] = ['.jpg', '.png', '.gif', '.jpeg']
app.config["UPLOAD_PATH"] = 'static/images'
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
mail = Mail(app)


# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("You're not authorised to do that.")
            return redirect(url_for("homepage"))
        return f(*args, **kwargs)
    return decorated_function


# 404 redirect
@app.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404


# -------------------------ADMIN BITS------------------------ #

@app.route("/register", methods=["GET", "POST"])
def register():

    if session.get('user'):
        return redirect(url_for("login"))

    if request.method == "POST":
        # checks if username exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "is_admin": False
        }
        mongo.db.users.insert_one(register)

        # put the new user into the session cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("admin", username=session["user"]))

    return render_template("register.html")


# Route for user's admin page
@app.route("/admin/<username>", methods=["GET", "POST"])
@login_required
def admin(username):

    # finds session users info from the database and retrieves username
    username = mongo.db.users.find_one(
        {"username": session["user"]})

    if session["user"]:
        return render_template("admin.html", username=username)

    return redirect(url_for("login"))


# ---------------------LOGIN AND LOGOUT--------------------- #


# Route for member login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        # checks if username exists in the database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for(
                    "admin", username=session["user"]))
            else:
                # invalid password
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            # invalid username
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Route for user logout
@app.route("/logout")
def logout():

    # logs user out and removes session cookies
    flash("You have been logged out")
    session.pop("user")

    return redirect(url_for("homepage"))


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


# Route for adding a new book
@app.route("/add_book", methods=["GET", "POST"])
@login_required
def add_book():

    if request.method == "POST":
        uploaded_file = request.files['cover']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
                abort(400)
            uploaded_file.save(
                os.path.join(app.config["UPLOAD_PATH"], filename))
        add_book = {
            "book_name": request.form.get("book_name"),
            "book_author": request.form.get("book_author"),
            "series_name": request.form.get("series_name"),
            "series_number": request.form.get("series_number"),
            "chronological_number": request.form.get("chronological_number"),
            "tagline": request.form.get("tagline"),
            "desc_p1": request.form.get("desc_p1"),
            "desc_p2": request.form.get("desc_p2"),
            "desc_p3": request.form.get("desc_p3"),
            "cover": f"/static/images/{uploaded_file.filename}",
            "link_1": request.form.get("link_1"),
            "link_2": request.form.get("link_2"),
            "link_3": request.form.get("link_3"),
            "ISBN": request.form.get("ISBN"),
            "is_ebook": request.form.get("is_ebook"),
            "is_paperback": request.form.get("is_paperback"),
            "is_hardback": request.form.get("is_hardback"),
            "is_audiobook": request.form.get("is_audiobook"),
        }
        mongo.db.books.insert_one(add_book)

        flash("Book Successfully Added")
        return redirect(url_for("books"))

    return render_template("add_book.html")


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


@app.route("/contact", methods=['GET', 'POST'])
def contact():

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        msg = Message(subject=f"Mail from {name}",
                      body=f"Name: {name}\n Email: {email}\n Msg: {message}",
                      sender=mail_username,
                      recipients=['contact@robertclarkauthor.com'])
        mail.send(msg)
        flash("Email sent!")
        return redirect(url_for("homepage"))

    return render_template("contact.html")


# Don't forget to put debug in if development var
if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True
    )
