import os
from flask import Flask, render_template
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


# --------------------------HOMEPAGE------------------------- #


@app.route("/")
@app.route("/homepage")
def homepage():
    return render_template("index.html")


# --------------------------BOOKS---------------------------- #


@app.route("/books")
def books():
    return render_template("books.html")


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
