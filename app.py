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
    ratings = mongo.db.books.find().sort("rating", -1)[:5]
    return render_template("index.html", books=books, ratings=ratings)


@app.route("/register", methods=["GET", "POST"])
# function for a user to register an account
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
# function to log a registered user into their profile
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
# function displays the users profile with the users reviews
def profile(username):
    if session:
        books = mongo.db.books.find()
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        # added defensive programming so if a user logged out and
        # pressed back it would take them to the log in screen
        if session["user"]:
            return render_template(
                "profile.html", username=username, books=books)
    return redirect(url_for("login"))


# function to log user out by clearing session user data cookie
@app.route("/logout")
# function to log the user out
def logout():
    flash("You have been logged out! ")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/reviews")
# function displays all the reviewed books
def reviews():
    books = list(mongo.db.books.find())
    return render_template("reviews.html", books=books)


@app.route("/reviews/<book_id>")
# function for the user to view a selected review
def display_book(book_id):
    book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
    return render_template("display_book.html", book=book)


@app.route("/add_review", methods=["GET", "POST"])
# function for the user to create their review
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

    # added defensive programming to stop
    # an error when logged out and returning to this page
    elif session:
        genres = mongo.db.genres.find().sort("genre_name", 1)
        return render_template("add_review.html", genres=genres)

    else:
        return redirect(url_for("login"))


@app.route("/edit_review/<book_id>", methods=["GET", "POST"])
# a function for a user to edit their submitted review
def edit_review(book_id):
    # added defensive programming to stop
    # an error when logged out and returning to this page
    if session:
        # if a user edits a review it will send them back to their profile page
        if request.method == "POST":
            submit = {
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
            mongo.db.books.update({"_id": ObjectId(book_id)}, submit)
            flash("Your review has been edited successfully")
            return redirect(url_for('profile', username=session['user']))

        book = mongo.db.books.find_one({"_id": ObjectId(book_id)})
        genres = mongo.db.genres.find().sort("genre_name", 1)
        return render_template("edit_review.html", book=book, genres=genres)

    else:
        return redirect(url_for("login"))


@app.route("/delete_review/<book_id>")
# function for a user to delete a users review
def delete_review(book_id):
    if session["user"]:
        mongo.db.books.remove({"_id": ObjectId(book_id)})
        flash("Your Review was successfully removed")
        return redirect(url_for('profile', username=session['user']))

    else:
        return redirect(url_for("login"))


@app.route("/manage_genres")
# function to open the manage genres page
def manage_genres():
    # added defensive programming to stop
    # an error when logged out and returning to this page
    if session:
        genres = mongo.db.genres.find().sort("genre_name")
        return render_template("manage_genres.html", genres=genres)

    else:
        return redirect(url_for("login"))


@app.route("/add_genre", methods=["GET", "POST"])
# function to add a new genre to the database
def add_genre():
    # check to ensure only admin can add a genre
    if session["user"] == "admin":
        if request.method == "POST":
            genre = {
               "genre_name": request.form.get("genre_name")
            }
            mongo.db.genres.insert(genre)
            flash("New Genre Added!")
            return redirect(url_for("manage_genres"))

        return render_template("add_genre.html")
    else:
        return redirect(url_for("login"))


@app.route("/edit_genre/<genre_id>", methods=["GET", "POST"])
# function for editing the select genre
def edit_genre(genre_id):
    # validation check to ensure user is logged in
    if session:
        if session["user"]:
            if request.method == "POST":
                submit = {
                    "genre_name": request.form.get("genre_name")
                }
                mongo.db.genres.update({"_id": ObjectId(genre_id)}, submit)
                flash("Genre Successfully Updated!")
                return redirect(url_for('manage_genres'))

        genre = mongo.db.genres.find_one({"_id": ObjectId(genre_id)})
        return render_template("edit_genre.html", genre=genre)

    else:
        return redirect(url_for("login"))


@app.route("/delete_genre/<genre_id>")
# function to delete a selected genre
def delete_genre(genre_id):
    # validation check
    if session:
        mongo.db.genres.remove({"_id": ObjectId(genre_id)})
        flash("Genre Successfully Removed!")
        return redirect(url_for("manage_genres"))

    else:
        return redirect(url_for("login"))


@app.route("/search", methods=["GET", "POST"])
# function for search feature
def search():
    query = request.form.get("query")
    books = list(mongo.db.books.find({"$text": {"$search": query}}))
    return render_template("reviews.html", books=books)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
