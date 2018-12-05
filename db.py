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

    command = "CREATE TABLE RVRest (username TEXT, restaurant TEXT, id INTEGER)"
    c.execute(command)

    command = "CREATE TABLE RVRec (username TEXT, recipe TEXT, id INTEGER)"
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

def add_fav(user, name_fav, table_name):
    ''' add a new favorite associated with the user to the corresponding table '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if (not check_exist(user, name_fav, table_name)):
        c.execute("INSERT INTO {} VALUES(?, ?)".format(table_name), (user, name_fav))
        db.commit()
        db.close()

def add_RV(user, name_RV, table_name): #limit rv's to 10
    ''' update the user's recently viewed list '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #gets current max id
    if (not check_exist(user, name_RV, table_name)):
        row_count = c.execute("SELECT COUNT(*) FROM RVRest WHERE username = '{}'".format(user)).fetchone()[0]
        print(row_count)
        if (row_count > 10):
            remove_oldest_entry(user, table_name)
        max_id = c.execute("SELECT MAX(id) FROM {} WHERE username = '{}'".format(table_name, user)).fetchone()[0]
        print(max_id)
        if (max_id == None):
            next_id = 0
        else:
            next_id = max_id + 1
        c.execute("INSERT INTO {} VALUES(?, ?, ?)".format(table_name), (user, name_RV, next_id))
    db.commit()
    db.close()

def get_fav(user, table_name):
    ''' retrieve a list of the user's favorites for given type '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    fav_data = []
    if (table_name == "favRest"):
        info_data = "restaurant"
    else:
        info_data = "recipe"

    temp = c.execute("SELECT {} FROM {} WHERE username = '{}'".format(info_data, table_name, user)).fetchall()
    for entry in temp:
        fav_data.append(entry[0])
    return fav_data

def get_RV(user, table_name):
    ''' retrieve the user's recently viewed list '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    RV_data = {}
    if (table_name == "favRest" or table_name == "RVRest"):
        info_data = "restaurant"
    else:
        info_data = "recipe"

    temp = c.execute("SELECT {},id from {} WHERE username = '{}'".format(info_data, table_name, user)).fetchall()
    for entry in temp:
        #print(entry[0]) -> info_data
        #print(entry[1]) -> id
        RV_data[entry[0]] = entry[1]
        ret_data = sorted(RV_data, key = RV_data.__getitem__)
    return ret_data


def check_exist(user, name_data, table_name):
    ''' check if an entry is already in the user's favorites or recently viewed '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (table_name == "favRest" or table_name == "RVRest"):
        info_data = "restaurant"
    else:
        info_data = "recipe"

    #print("table: %s, info: %s" % (table_name, info_data))
    ret_val = c.execute("SELECT {} from {} WHERE username = '{}'".format(info_data, table_name, user))
    for each in ret_val:
        #print(each)
        if (each[0] == name_data):
            print("repeated entry!")
            return True
    return False

def remove_oldest_entry(user, table_name):
    ''' removes oldest entry in a table from the database '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (table_name == "RVRest"):
        info_data = "restaurant"
    else:
        info_data = "recipe"

    min_id = c.execute("SELECT MIN(id) FROM {} WHERE username = '{}'".format(table_name, user)).fetchone()[0]
    c.execute("DELETE FROM {} WHERE username = '{}' and id = {}".format(table_name, user, min_id))
    # top_entry = c.execute("SELECT {} FROM {} WHERE username = '{}' and id = {}".format(info_data, table_name, user, min_id)).fetchone()[0]
    # print("deleting:")
    # print(top_entry)

    db.commit()
    db.close()

def remove_fav(user, rmv_data, table_name):
    ''' Remove entry in one of the favorites tables '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (table_name == "favRest"):
        # print("restaurant")
        info_data = "restaurant"
    else:
        info_data = "recipe"

    c.execute("DELETE FROM {} WHERE username = '{}' and {} = '{}'".format(table_name, user, info_data, rmv_data))

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
