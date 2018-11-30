#RGB
#Bamba Shin, Soojin Choi, Kenny Li, Joyce Liao
#Project 1
import os

from flask import Flask, request, render_template, \
flash, session, url_for, redirect

import db
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
    if db.auth_user(request.args["user"], request.args["password"]):
        session["logged_in"] = request.args["user"]
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
#Flashes message accordingly if user exists or args isn't filled
@app.route("/adduser")
def add_user():
    if(not request.args["user"].strip() or not request.args["password"] or not request.args["confirm_password"]):
        flash("Please fill in all fields")
        return redirect(url_for("register"))

    if(db.check_user(request.args["user"])):
        flash("User already exists")
        return redirect(url_for("register"))

    if(request.args["password"] != request.args["confirm_password"]):
        flash("Passwords don't match")
        return redirect(url_for("register"))

    db.add_user(request.args["user"], request.args["password"])
    session["logged_in"] = request.args["user"]
    return redirect(url_for("home"))

#---------- Home Route ----------
#Displays home page
@app.route("/home")
def home():
    return render_template("home.html", user=session["logged_in"])

#---------- Logout Route ----------
#Logs the user out and removes session
@app.route("/logout")
def logout():
    session.pop("logged_in")
    return redirect(url_for("login"))

#----------- Restaurants Routes-----
@app.route("/restGo")
def restGo():
	args = {}
	args['user'] = session['logged_in']
	args['fav_rest'] = ['this','is','a','list']
	args['rv_rest'] = ['this','is','a','list']
	return render_template("restaurant.html",**args)


#----------- Recipe Routs -----------
@app.route("/recGo")
def recGo():
	args = {}
	args['user'] = session['logged_in']
	args['fav_rec'] = ['this','is','a','list']
	args['rv_rec'] = ['this','is','a','list']
	return render_template("recipe.html", **args)
if __name__ == "__main__":
    app.debug = True
    app.run()
