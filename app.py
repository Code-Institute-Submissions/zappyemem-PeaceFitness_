import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.getenv("MONGO_DBNAME")
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/fitness_updates")
def fitness_updates():
    return render_template("fitness_updates.html")

@app.route("/trainings")
def trainings():
    trainings = list(mongo.db.trainings.find())
    return render_template("trainings.html", trainings=trainings)

@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    trainings = list(mongo.db.trainings.find({"$text": {"$search": query}}))
    return render_template("trainings.html", trainings=trainings)
    

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # To check if username already exist in DB
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username Exists Already")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        } 
        mongo.db.users.insert_one(register) 

        # New user 'Session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # confirm if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # confirm hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Hello, {}".format
                      (request.form.get("username")))
                    return redirect(url_for
                      ("profile", username=session["user"]))
            else:
                # wrong password match
                flash("Wrong Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Wrong Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # To get the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # To get user from session cookie
    flash("You have logged out")
    session.pop("user")
    return redirect(url_for("login"))




if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)