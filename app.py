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


@app.route("/add_exercise", methods=["GET", "POST"])
def add_exercise():
    if request.method == "POST":

        training = {
            "category_name": request.form.get("category_name"),
            "program_name": request.form.get("program_name"),
            "exercise_description": request.form.get("exercise_description"),
            "training_date": request.form.get("training_date"),
            "created_by": session["user"]
        }

        mongo.db.trainings.insert_one(training)
        flash("Account Update Successfully ")
        return redirect(url_for("trainings"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("update_account.html", categories=categories)


@app.route("/edit_account/<training_id>", methods=["GET", "POST"])
def edit_account(training_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name"),
            "program_name": request.form.get("program_name"),
            "exercise_description": request.form.get("exercise_description"),
            "trainig_date": request.form.get("training_date"),
            "created_by": session["user"]
        }
        
        mongo.db.tips.update({"_id": ObjectId(training_id)}, submit)
        flash("Account Updated Successfully ")

    training = mongo.db.tips.find_one({"_id": ObjectId(training_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_account.html", training=training, categories=categories)


@app.route("/delete_training/<training_id>")
def delete_training(training_id):
    mongo.db.trainings.remove({"_id": ObjectId(training_id)})
    flash("Training Deleted Succesfully")
    return redirect(url_for("trainings"))

@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)

@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.insert_one(category)
        flash("New Category Added")
        return redirect(url_for("get_categories"))

    return render_template("add_categories.html")

@app.route("/edit_category/<category_id>",methods=["GET", "POST"])
def edit_category(category_id):
    if request.method == "POST":
        submit = {
            "category_name": request.form.get("category_name")
        }
        mongo.db.categories.update({"_id": ObjectId(category_id)}, submit)
        flash("Category Updated Successfully")
        return redirect(url_for("get_categories"))

    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    return render_template("edit_category.html", category=category)

@app.route("/delete_category/<category_id>")
def delete_category(category_id):
    
    mongo.db.categories.remove({"_id": ObjectId(category_id)})
    flash("Category Successfully Deleted")
    return redirect(url_for("get_categories")) 





if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)