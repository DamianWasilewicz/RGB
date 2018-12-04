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

def add_fav(user, name_fav, type_fav):
    ''' add a new favorite associated with the user to the corresponding table '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    if (type_fav == "fav_rest"): #fav_rest
        c.execute("INSERT INTO favRest VALUES(?, ?)", (user, name_fav))
    else:
        c.execute("INSERT INTO favRec VALUES(?, ?)", (user, name_fav))
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
            remove_entry(user, table_name)
        max_id = c.execute("SELECT MAX(id) FROM {} WHERE username = '{}'".format(table_name, user)).fetchone()[0]
        print(max_id)
        if (max_id == None):
            next_id = 0;
        else:
            next_id = max_id + 1
        c.execute("INSERT INTO {} VALUES(?, ?, ?)".format(table_name), (user, name_RV, next_id))
    db.commit()
    db.close()

def get_fav(user, type_fav):
    ''' retrieve a list of the user's favorites for given type '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    fav_data = []
    if (type_fav == "fav_rest"):
        temp = c.execute("SELECT restaurant FROM favRest WHERE username = '{}'".format(user)).fetchall()
        for entry in temp:
            fav_data.append(entry[0])
    else:
        temp = c.execute("SELECT recipe FROM favRec WHERE username = '{}'".format(user)).fetchall()
        for entry in temp:
            fav_data.append(entry[0])
    return fav_data

def get_RV(user, type_RV):
    ''' retrieve the user's recently viewed list '''
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    RV_data = []
    if (type_RV == "RV_rest"):
        temp = c.execute("SELECT restaurant from RVRest WHERE username = '{}'".format(user)).fetchall()
        for entry in temp:
            RV_data.append(entry[0])
    else:
        temp = c.execute("SELECT recipe from RVRec WHERE username = '{}'".format(user)).fetchall()
        for entry in temp:
            RV_data.append(entry[0])
    return RV_data


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
            return True
    return False

def remove_entry(user, table_name):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if (table_name == "favRest" or table_name == "RVRest"):
        info_data = "restaurant"
    else:
        info_data = "recipe"

    top_entry = c.execute("SELECT {} FROM {} WHERE username = '{}' and id = MIN(id)".format(info_data, table_name, user)).fetchone()[0]
    print("deleting:")
    print(top_entry)

    db.close()


# =========== db function tests ===========
# createTable()
# add_fav("b", "fav1", "fav_rest")
# add_fav("a", "fav5", "fav_rest")
# add_fav("a", "fav12", "fav_rest")
# add_fav("a", "fav1", "fav_rest")
# add_RV("a", "RV0", "RV_rest")
add_RV("a", "RV2", "RVRest")
# add_RV("a", "RV58", "RV_rec")
add_RV("a", "RV3", "RVRest")
# print("a fav rest:")
# print(get_fav("a", "fav_rest"))
# print("a RV rest:")
print(get_RV("a", "RV_rest"))
# print("a RV rec:")
# print(get_RV("a", "RV_rec"))
# print("b RV rest:")
# print(get_RV("b", "RV_rest"))
# print("b RV rec:")
# print(get_RV("b", "RV_rec"))
# print("b fav rest:")
# print(get_fav("b", "fav_rest"))
# print(check_exist("a", "fav1", "fav_rest"))
# print(check_exist("a", "fav3", "fav_rest"))
# remove_entry("a", "fav_rest")
