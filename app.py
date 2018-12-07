#RGB
#Bamba Shin, Soojin Choi, Kenny Li, Joyce Liao
#Project 1
import os

from flask import Flask, request, render_template, \
     flash, session, url_for, redirect

from util import db, info


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

#---------- Logout Route ----------
#Logs the user out and removes session

@app.route("/logout")
def logout():
    try:
        session.pop("logged_in")
    finally:
        return redirect(url_for("login"))


#---------- Main Page ----------

@app.route("/home")
def home():
    try:
        return render_template("home.html", user=session["logged_in"])
    except:
        return redirect(url_for(login))

@app.route("/fav")
def show_favorites():
    return render_template("favorites.html", user=session["logged_in"], recipe=db.get_fav(session["logged_in"], "favRec"))
#----------- Recipe Routes-----

#Displays home page
@app.route("/recipePath")
def recipePath():
    """Ask user for an ingredient the recipe has to include."""
    # data = db.get_fav(session["logged_in"], "favRec")
    # print(data)
    return render_template("recipePath.html", user=session["logged_in"], favs = db.get_fav(session["logged_in"], "favRec"))

@app.route("/processIngredient")
def processIngredient():
    """Display a list of recipes based on user input."""
    if request.args["ingredient"].strip() == "":
        flash("Please insert text")
        return redirect(url_for("recipePath"))
    return render_template("recipeList.html", recipeData=info.searchRecs(request.args["ingredient"]), user=session["logged_in"])

@app.route("/recipe")
def recipe():
    """Display content of a selected recipe."""
    # data[0] = title
    # data[1] = list of ingredients
    # data[2] = recipe link
    # data[3] = img url
    data = info.getRecs(request.args["id"])
    recID = request.args["id"]
    fav_data = data[0].replace(" ", "{~}") + "||" + recID
    db.add_RV(session["logged_in"], data[0], "RVRec", recID)
    fav_rmv = db.check_exist(session["logged_in"], data[0], "favRec")
    return render_template("recipe.html", recipe= data, user=session["logged_in"], fav = fav_data, fav_or_rmv = fav_rmv, id=recID)

@app.route("/addFav", methods = ["GET", "POST"])
def addFav():
    # print ("request.args: " )
    # print ( request.args )
    # print ( "\n ------------")
    # print ("request.form: " )
    # print ( request.form )
    # print ( "\n -----------")
    for each in request.form:
        # print(each)
        if (request.form[each] == 'Add to favorites'):
            fav_data = each
            each = each.split("||")
            recID = each[1]
            info_name = each[0].replace("{~}", " ")
            # print(each[0])
    data = info.getRecs(recID)
    username = session["logged_in"]
    db.add_fav(username, info_name, recID, "favRec")
    return redirect(url_for("recipe", recipe= data, user=session["logged_in"], fav = fav_data, fav_or_rmv = True, id=recID))

@app.route("/removeFav", methods = ["GET", "POST"])
def removeFav():
    for each in request.form:
        # print(each)
        if (request.form[each] == 'Remove from favorites'):
            fav_data = each
            each = each.split("||")
            recID = each[1]
            info_name = each[0].replace("{~}", " ")
    data = info.getRecs(recID)
    username = session["logged_in"]
    db.remove_fav(username, info_name, "favRec")
    return redirect(url_for("recipe", recipe= data, user=session["logged_in"], fav = fav_data, fav_or_rmv = False, id=recID))

#----------- USDA Routes-----
@app.route("/processNutrients")
def processNutrients():
    if request.args["ingredient"].strip() == "":
        flash("Please insert text")
        data = info.getRecs(request.args["id"])
        recID = request.args["id"]
        fav_data = data[0].replace(" ", "{~}") + "||" + recID
        db.add_RV(session["logged_in"], data[0], "RVRec", recID)
        fav_rmv = db.check_exist(session["logged_in"], data[0], "favRec")
        return redirect(url_for("recipe", recipe=data, user=session["logged_in"], fav = fav_data, fav_or_rmv = fav_rmv, id=recID))
    return render_template("ingredientList.html", ingredientData = info.searchIngredient(request.args['ingredient']), user=session["logged_in"])

@app.route("/ingredient")
def ingredient():
	return render_template("ingredient.html", ingredient = info.getInfo(request.args['ndbno']), user=session["logged_in"])

#----------- Restaurants Routes-----
@app.route("/restaurantPath")
def restaurantPath():
    """Ask user to enter a city name."""
    return render_template("restaurantPath.html", user=session["logged_in"])

@app.route("/processCity")
def processCity():
    """Show a list of cities the user can select."""
    if request.args["city"].strip() == "":
        flash("Please insert text")
        return redirect(url_for("restaurantPath"))
    return render_template("cityList.html", cityList=info.getTypeDict(request.args["city"], "cities"), user=session["logged_in"])

@app.route("/city")
def city():
    """Show the choices for establishments or cuisines."""
    return render_template("restaurantQuery.html", city=request.args["id"],
    establishmentList=info.getTypeDict(request.args["id"],"establishments"),
    cuisineList=info.getTypeDict(request.args["id"],"cuisines"), user=session["logged_in"])

@app.route("/processQuery")
def processQuery():
    """Show a list of restaurants that match the user's preferences."""
    establishment = request.args["establishment"]
    cuisine = request.args["cuisine"]
    if establishment == "none":
        establishment = None
    if cuisine == "none":
        cuisine = None
    return render_template("restaurant.html", restaurantList=info.searchRestuarant(request.args["city"], establishment, cuisine), user=session["logged_in"])

if __name__ == "__main__":
    app.debug = True
    app.run()
