from urllib import request
import json

f2fKey = "50eb99e18a32f2eb95b721b09a2c4402"
zomatoKey = "50427fa83b5eda149411a00deb4cedc5"
yelpKey = "WZvWvogiVfxzNrpWipq63HV1fAJZKU4R-kDfewNhYQssKpX\
jFCbbdwe0IGQW7Bh86cEEL7Xh5Yb8bgGOfgYaCJQ5BXt2-n0v4ymnkdL49ou1Ot1vNDBI__0egaj0W3Yx"
usdaKey = "LSwsFBYAj6DAx8ChR6hy5420iIX8IyQCPoDMGt3G"


'''
the dictionary depends on the type given: cities, establishments or cuisines
returns the dictionary based on the type specified {name of type:zomato specific id}
'''
def getTypeDict(query, type):
    typeDict = dict() #creates a dictionary of type
    if (type == "cities"):
        qString = "/cities?q=" + query
    elif (type == "establishments"):
        qString = "/establishments?city_id=" + query
    else:
        qString = "/cuisines?city_id=" + query
    zomatoUrl = request.Request("https://developers.zomato.com/api/v2.1" + qString)
    zomatoUrl.add_header("user-key", zomatoKey)
    zomatoUrl.add_header('User-Agent','Mozilla/5.0')
    data = json.loads(request.urlopen(zomatoUrl).read())
    if (type == "cities"):
        for cityList in data["location_suggestions"]:
            typeDict[cityList["name"]] = cityList["id"]
    elif (type == "establishments"):
        for establishmentList in data["establishments"]:
            typeDict[establishmentList["establishment"]["name"]] = establishmentList["establishment"]["id"]
    elif (type == "cuisines"):
        for cuisineList in data["cuisines"]:
            typeDict[cuisineList["cuisine"]["cuisine_name"]] = cuisineList["cuisine"]["cuisine_id"]
    return typeDict

def searchRestuarant(city, establishment, cuisine):
    qString = "/search?entity_id=" + city + "&entity_type=city"
    if establishment is not None:
        qString += "&establishment_type=" + establishment
    if cuisine is not None:
        qString += "&cuisines=" + cuisine
    zomatoUrl = request.Request("https://developers.zomato.com/api/v2.1" + qString)
    zomatoUrl.add_header("user-key", zomatoKey)
    zomatoUrl.add_header('User-Agent','Mozilla/5.0')
    data = json.loads(request.urlopen(zomatoUrl).read())
    return data

# print(getTypeDict("new","cities"))
# print(getTypeDict("1","establishments"))
# print(getTypeDict("1","cuisines"))
print(searchRestuarant("1","1","1"))
