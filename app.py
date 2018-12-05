#RGB
#Bamba Shin, Soojin Choi, Kenny Li, Joyce Liao
#Project 1
import os

from flask import Flask, request, render_template, \
     flash, session, url_for, redirect

import db, info


app = Flask(__name__)

app.secret_key = os.urandom(32)

#---------- Login Routes ----------
#Sends the user to the login page if they are logged in
#If not they have to login or register
@app.route("/")
def login():
    if "logged_in" in session:
        return redirect(url_for("recipePath"))
    return render_template("login.html")

#Authenticates user and creates a session
@app.route("/auth")
def authenticate():
    if db.auth_user(request.args["user"], request.args["password"]):
        session["logged_in"] = request.args["user"]
        return redirect(url_for("recipePath"))
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

#---------- Logout Route ----------
#Logs the user out and removes session

@app.route("/logout")
def logout():
    session.pop("logged_in")
    return redirect(url_for("login"))


#----------- Recipe Routes-----

#Displays home page
@app.route("/recipePath")
def recipePath():
    return render_template("recipePath.html", user=session["logged_in"])

@app.route("/processIngredient")
def processIngredient():
	return render_template("recipeList.html", recipeData=info.searchRecs(request.args["ingredient"]))

@app.route("/recipe")
def recipe():
    return render_template("recipe.html", recipe=info.getRecs(request.args["id"]))
#----------- Restaurants Routes-----

@app.route("/restaurantPath")
def restaurantPath():
    return render_template("restaurantPath.html")

@app.route("/processCity")
def processCity():
	return render_template("cityList.html", cityList=info.getTypeDict(request.args["city"], "cities"))

@app.route("/city")
def city():
    return render_template("restaurantQuery.html", city=request.args["id"], 
    establishmentList=info.getTypeDict(request.args["id"],"establishments"),
    cuisineList=info.getTypeDict(request.args["id"],"cuisines"))

@app.route("/processQuery")
def processQuery():
    establishment = request.args["establishment"]
    cuisine = request.args["cuisine"]
    if establishment == "none":
        establishment = None
    if cuisine == "none":
        cuisine = None
    return render_template("restaurant.html", restaurantList=info.searchRestuarant(request.args["city"], establishment, cuisine))
#----------- USDA Routes-----




if __name__ == "__main__":
    app.debug = True
    app.run()
