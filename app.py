import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    books = list(mongo.db.books.find())
    return render_template("index.html", books=books)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # conditional statement to check if username is already registered
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # check to see if passwords match
        if (request.form.get("password").lower() !=
                request.form.get("confirm-password").lower()):
            flash("Passwords must match!")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                        request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        return render_template("profile.html", username=username)
    return redirect(url_for("login"))


# function to log user out by clearing session user data cookie
@app.route("/logout")
def logout():
    flash("You have been logged out! ")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/reviews")
def reviews():
    books = list(mongo.db.books.find())
    return render_template("reviews.html", books=books)


@app.route("/reviews/<book_id>")
def display_book(book_id):
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    return render_template("display_book.html", book=book)


@app.route("/add_review", methods=["GET", "POST"])
def add_review():
    if request.method == "POST":
        review = {
            "book_name": request.form.get("book_name"),
            "book_author": request.form.get("book_author"),
            "genre": request.form.get("genre"),
            "rating": request.form.get("rating"),
            "review_title": request.form.get("review_title"),
            "review": request.form.get("review"),
            "reviewed_by": session["user"],
            "image_url": request.form.get("image_url"),
            "purchase_link": request.form.get("purchase_link")
        }
        mongo.db.books.insert_one(review)
        flash("Your review has been recieved!")
        return redirect(url_for("reviews"))
    genres = mongo.db.genres.find().sort("genre_name", 1)
    return render_template("add_review.html", genres=genres)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
