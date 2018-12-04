from urllib import request
import json

with open('api.json', 'r') as file:
    api_dict = json.load(file)

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
    zomatoUrl.add_header("user-key", api_dict["zomato"])
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

'''
returns 10 restuarants that fall into the criteria of city, establishment and cuisine
single restuarant list is [name, address, location]
'''
def searchRestuarant(city, establishment, cuisine):
    qString = "/search?entity_id=" + city + "&entity_type=city&count=10"
    if establishment is not None:
        qString += "&establishment_type=" + establishment
    if cuisine is not None:
        qString += "&cuisines=" + cuisine
    zomatoUrl = request.Request("https://developers.zomato.com/api/v2.1" + qString)
    zomatoUrl.add_header("user-key", api_dict["zomato"])
    zomatoUrl.add_header('User-Agent','Mozilla/5.0')
    data = json.loads(request.urlopen(zomatoUrl).read())
    retList = list()
    for restuarantList in data["restaurants"]:
        restuarantListInfo = restuarantList["restaurant"] #List of restaurant info
        retList.append([restuarantListInfo["name"], \
                         restuarantListInfo["location"]["address"], \
                         restuarantListInfo["user_rating"]["aggregate_rating"]])
    return retList

# print(getTypeDict("new","cities"))
# print(getTypeDict("1","establishments"))
# print(getTypeDict("1","cuisines"))
print(searchRestuarant("1","1","1"))
