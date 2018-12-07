import sqlite3
DB_FILE="data/food.db"

def createTable():
    """Creates the two main data tables for users and list of stories."""
    db = sqlite3.connect("../"+DB_FILE)
    c = db.cursor()
    command = "CREATE TABLE users (username TEXT, password TEXT)"
    c.execute(command)

    command = "CREATE TABLE favRec (username TEXT, recipe TEXT, id TEXT)"
    c.execute(command)

    command = "CREATE TABLE RVRec (username TEXT, recipe TEXT, id INTEGER, recID TEXT)"
    c.execute(command)

    db.commit() #save changes
    db.close()  #close database

#createTable()

def add_user(username, password):
    """Insert credentials for newly registered user into database."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute("INSERT INTO users VALUES(?, ?)", (username, password))
    db.commit() #save changes
    db.close()  #close database

def auth_user(username, password):
    """Authenticate a user attempting to log in."""
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
    """Check if a username has already been taken when registering."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for entry in c.execute("SELECT users.username FROM users"):
        if(entry[0] == username):
            db.close()
            return True
    db.close()
    return False

def add_fav(user, name_fav, id):
    """Add a new favorite associated with the user to the corresponding table."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #allows to add favorite if it does not already exist
    if (not check_exist(user, name_fav, "favRec")):
        c.execute("INSERT INTO favRec VALUES(?, ?, ?)", (user, name_fav, id))
        db.commit()
        db.close()
        return True
    #print(get_fav)
    db.close()
    return False

def add_RV(user, name_RV, rec_id): #limit rv's to 10
    """Update the user's recently viewed list."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    error = True
    #gets current max id
    if (not check_exist(user, name_RV, "RVRec")):
        row_count = c.execute("SELECT COUNT(*) FROM RVRec WHERE username = '{}'".format(user)).fetchone()[0]
        print(row_count)
        #remove oldest entry if there are 10 already
        if (row_count > 9):
            remove_oldest_entry(user)
        max_id = c.execute("SELECT MAX(id) FROM RVRec WHERE username = '{}'".format(user)).fetchone()[0]
        # print(max_id)
        if (max_id == None):
            next_id = 0
        else:
            next_id = max_id + 1
        #add most recent
        c.execute("INSERT INTO RVRec VALUES(?, ?, ?, ?)", (user, name_RV, next_id, rec_id))
        error = False
    db.commit()
    db.close()
    return error

def get_fav(user):
    """Retrieve a list of the user's favorites for given type."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    fav_data = []

    temp = c.execute("SELECT recipe, id FROM favRec WHERE username = '{}'".format(user)).fetchall()
    for entry in temp:
        fav_data.append(entry)
    db.close()
    return fav_data

def get_RV(user):
    """Retrieve the user's recently viewed list."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    RV_data = {}

    temp = c.execute("SELECT recipe ,id, recID from RVRec WHERE username = '{}'".format(user)).fetchall()
    for entry in temp:
        #print(entry[0]) -> info_data
        #print(entry[1]) -> id
        RV_data[entry[1]] = [entry[0], entry[2]]
    #sort data by its id
    temp_data = sorted(RV_data, reverse = True)
    #print(temp_data)
    ret_data = []
    for each in temp_data:
        smth = RV_data.get(each, "")
        ret_data.append( smth )
    #print("ret_data:")
    #print(ret_data)
    db.close()
    return ret_data

def check_exist(user, name_data, table_name):
    """Check if an entry is already in the user's favorites or recently viewed."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #print("table: %s, info: %s" % (table_name, info_data))
    ret_val = c.execute("SELECT recipe from {} WHERE username = '{}'".format( table_name, user))
    for each in ret_val:
        #print(each)
        #go through list to see if any entry matches given entry
        if (each[0] == name_data):
            # print("repeated entry!")
            db.close()
            return True
    db.close()
    return False

def remove_oldest_entry(user):
    """Removes oldest entry in a table from the database."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    min_id = c.execute("SELECT MIN(id) FROM RVRec WHERE username = '{}'".format( user)).fetchone()[0]
    c.execute("DELETE FROM RVRec WHERE username = '{}' and id = {}".format( user, min_id))
    # print("deleting:")
    # print(top_entry)

    db.commit()
    db.close()

def remove_fav(user, rmv_data):
    """Remove entry in one of the favorites tables."""
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute("DELETE FROM favRec WHERE username = '{}' and recipe = '{}'".format(user, rmv_data))

    db.commit()
    db.close()


# =========== db function tests ===========
# createTable()
#
# add_fav("a", "fav0", "favRest")
# add_fav("a", "fav1", "favRest")
# add_fav("a", "fav2", "favRest")
# add_fav("b", "fav1", "favRest")
# print(get_fav("a", "favRest"))
# print("_____________________________")

# add_RV("a", "RV0", "RVRest")
# add_RV("a", "RV1", "RVRest")
# add_RV("a", "RV3", "RVRest")
# add_RV("a", "RV10", "RVRest")
# add_RV("a", "RV4", "RVRest")
# add_RV("a", "RV89", "RVRest")
# add_RV("a", "RV6", "RVRest")
# add_RV("a", "RV11", "RVRest")
# add_RV("a", "RV46", "RVRest")
# add_RV("a", "RV12", "RVRest")
# add_RV("a", "RV43", "RVRest")
# add_RV("a", "RV47", "RVRest")

# add_RV("a", "RV2", "RVRec")
# print(get_RV("a", "RVRest"))
#
# add_RV("a", "RV89", "RVRest")
# print("_____________________________")


# print("a RV rec:")
# print(get_RV("a", "RVRec"))
# print("b RV rest:")
# print(get_RV("b", "RVRest"))
# print("b RV rec:")
# print(get_RV("b", "RVRec"))
# print("b fav rest:")
# print(get_fav("b", "favRest"))
# print(check_exist("a", "fav1", "favRest"))
# print(check_exist("a", "fav3", "favRest"))
# remove_oldest_entry("a", "RVRest")
# print(get_RV("a", "RVRest"))
# remove_fav("a", "fav0", "favRest")
# print(get_fav("a", "favRest"))
