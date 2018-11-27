#Kenny Li
#SoftDev1 Pd8
import os
from urllib import request

from flask import Flask, request, render_template, \
flash, session, url_for, redirect

app = Flask(__name__)

app.secret_key = os.urandom(32)

#---------- Login Routes ----------
#Sends the user to the login page if they are logged in
#If not they have to login or register
@app.route("/")
def login():
    if "logged_in" in session:
        return redirect(url_for("home"))
    return render_template("login.html")

#Authenticates user and creates a session
@app.route("/auth")
def authenticate():
    if story.auth_user(request.form["user"], request.form["password"]):
        session["logged_in"] = request.form["user"]
        return redirect(url_for("home"))
    else:
        flash("username or password is incorrect")
        return redirect(url_for("login"))

#---------- Register Routes ----------
#Sends the user to the register page to create account
@app.route("/register")
def register():
    return render_template("register.html")

#Adds user to the database after they register
#Flashes message accordingly if user exists or form isn't filled
@app.route("/adduser")
def add_user():
    if(not request.form["user"].strip() or not request.form["password"] or not request.form["confirm_password"]):
        flash("Please fill in all fields")
        return redirect(url_for("register"))

    if(story.check_user(request.form["user"])):
        flash("User already exists")
        return redirect(url_for("register"))

    if(request.form["password"] != request.form["confirm_password"]):
        flash("Passwords don't match")
        return redirect(url_for("register"))

    #story.add_user(request.form["user"], request.form["password"])
    session["logged_in"] = request.form["user"]
    return redirect(url_for("home"))

#---------- Home Route ----------
#Displays home page
@app.route("/home")
def home():
    return render_template("home.html", user=session["logged_in"])

if __name__ == "__main__":
    app.debug = True
    app.run()
