from urllib import request
import json

f2fKey = "50eb99e18a32f2eb95b721b09a2c4402"
zomatoKey = "50427fa83b5eda149411a00deb4cedc5"
yelpKey = "WZvWvogiVfxzNrpWipq63HV1fAJZKU4R-kDfewNhYQssKpX\
jFCbbdwe0IGQW7Bh86cEEL7Xh5Yb8bgGOfgYaCJQ5BXt2-n0v4ymnkdL49ou1Ot1vNDBI__0egaj0W3Yx"
usdaKey = "LSwsFBYAj6DAx8ChR6hy5420iIX8IyQCPoDMGt3G"


'''
the dictionary depends on the type given: cities or establishments
returns the dictionary based on the type specified {name:id}
'''
def getTypeDict(query, type):
    typeDict = dict() #creates a dictionary of type
    if (type == "cities"):
        qString = "/cities?q=" + query
    elif (type == "establishments"):
        qString = "/establishments?city_id=" + query
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
    return typeDict

print(getTypeDict("new_york","cities"))
print(getTypeDict("1","establishments"))

# zomatoUrl = request.Request("https://developers.zomato.com/api/v2.1")
# cityString = "/cities?q="
# queryString = "/establishment/city_id=1"
# zomatoUrl.add_header("user-key", zomatoKey)
# zomatoUrl.add_header('User-Agent','Mozilla/5.0')
# data = json.loads(request.urlopen(zomatoUrl).read())
# print(data)
