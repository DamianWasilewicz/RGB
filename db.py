import sqlite3
DB_FILE="food.db"

def createTable():
    ''' creates the two main data tables for users and list of stories '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE users (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE favRest (username TEXT, restaurant TEXT)"
    c.execute(command)

    command = "CREATE TABLE favRec (username TEXT, recipe TEXT)"
    c.execute(command)

    command = "CREATE TABLE RVRest (username TEXT, restaurant TEXT)"
    c.execute(command)

    command = "CREATE TABLE RVRec (username TEXT, recipe TEXT)"
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database

# createTable()

def add_user(username, password):
    ''' insert credentials for newly registered user into database '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?, ?)", (username, password))
    db.commit() #save changes
    db.close()  #close database

def auth_user(username, password):
    ''' authenticate a user attempting to log in '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # user_info = c.execute("SELECT users.username, users.password FROM users WHERE username={} AND password={}".format(username, password))
    for entry in c.execute("SELECT users.username, users.password FROM users"):
        if(entry[0] == username and entry[1] == password):
            db.close()
            return True
    db.close()
    return False

def check_user(username):
    ''' check if a username has already been taken when registering '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for entry in c.execute("SELECT users.username FROM users"):
        if(entry[0] == username):
            db.close()
            return True
    db.close()
    return False

def add_fav(user, name_fav, type_fav):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if (type_fav == "fav_rest"): #fav_rest
        c.execute("INSERT INTO favRest VALUES(?, ?)", (user, name_fav))
    else:
        c.execute("INSERT INTO favRec VALUES(?, ?)", (user, name_fav))
    db.close()

def add_RV(user, name_RV, type_RV): #limit rv's to 10 
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if (type_RV == "RV_rest"): #fav_rest
        c.execute("INSERT INTO RVRest VALUES(?, ?)", (user, name_RV))
    else:
        c.execute("INSERT INTO RVRec VALUES(?, ?)", (user, name_RV))
    db.close()

    
#return a list for user

def get_fav(user, type_fav):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    fav_data = []
    if (type_fav == "fav_rest"):
        temp = c.execute("SELECT restaurant FROM favRest WHERE username = '"+user+"'").fetchall()
        for entry in temp:
            fav_data.append(entry[0])
    else:
        temp = c.execute("SELECT recipe FROM favRec WHERE username = '"+ user  +"' ").fetchall()
        for entry in temp:
            fav_data.append(entry[0])
    return fav_data

def get_RV(user, type_RV):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    RV_data = []
    if (type_RV == "RV_rest"):
        temp = c.execute("SELECT restaurant from RVRest where username =" + user).fetchall()
        for entry in temp:
            RV_data.append(entry[0])
    else:
        temp = c.execute("SELECT recipe from RVRec where username =" + user).fetchall()
        for entry in temp:
            RV_data.append(entry[0])
    return RV_data


def check_exist(user, name_data, type_data):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (type_data == "fav_rest"):
        table_name = "favRest"
        info_data = "restaurant"
    if (type_data == "fav_rec"):
        table_name = "favRec"
        info_data = "recipe"
    if (type_data == "RV_rest"):
        table_name = "RVRest"
        info_data = "restaurant"
    else: #RV_rec
        table_name = "RVRec"
        info_data = "recipe"
    
    ret_val = c.execute("SELECT (?) from (?) where username = '" + user+ "'", (info_data, table_name))    
    for each in ret_val:
        if (each[0] == name_data):
            return True
    return False

add_fav("b", "fav1", "fav_rest")
add_fav("a", "fav5", "fav_rest")
add_fav("a", "fav12", "fav_rest")
add_fav("a", "fav1", "fav_rest")
print(get_fav("a", "fav_rest"))
print(check_exist("a", "fav1", "fav_rest"))
