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

'''
given a list of ingredients
returns a dictionary of at most 30 top available recipes and id
'''
def searchRecs(ingredients):
	f2fUrl =  request.Request("https://www.food2fork.com/api/search?key=" + api_dict["f2f"] + "&q=" + ingredients, headers={'User-Agent': 'Mozilla/5.0'})
	data = json.loads(request.urlopen(f2fUrl).read())
	listOfRecs = data['recipes']
	recs = {}
	for rec in listOfRecs:
		recs[rec['title']] = rec['recipe_id']
	return recs

'''
given a recipe id from the F2F database, returns a list of ingredients that are needed in order to create the dish
'''
def getRecs(rec_id):
    f2fUrl =  request.Request("https://www.food2fork.com/api/get?key=" + api_dict["f2f"] + "&rId=" + rec_id, headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(request.urlopen(f2fUrl).read())
    return [data['recipe']['ingredients'],data['recipe']['source_url']]


'''
given an ingredient
returns a dictionary of at most 20 top results when searched for that ingredient paired with ndbno (USDA id)
'''
def searchIngredient(ingredient):
	usdaUrl = request.Request("https://api.nal.usda.gov/ndb/search/?format=json&sort=n&max=10&offset=0&ds=Standard%20Reference" + "&q=" + ingredient + "&api_key=" + api_dict["usda"], headers={'User-Agent': 'Mozilla/5.0'})
	#usdaUrl.add_header("q", ingredient)
	#usdaUrl.add_header("api_key", api_dict["usda"])
	#usdaUrl.add_header('User-Agent','Mozilla/5.0')
	data = json.loads(request.urlopen(usdaUrl).read())
	listOfIng = data['list']['item']
	ingreds = {}
	for ing in listOfIng:
		ingreds[ing['name']] = ing['ndbno']
	return ingreds

'''
given a valid ndbno id,
returns a dictionary with nutrient {name : nutrient value}
'''
def getInfo(ndbno):
	usdaUrl = request.Request("https://api.nal.usda.gov/ndb/V2/reports?type=b&format=json&" + "ndbno=" + ndbno + "&api_key=" + api_dict['usda'],  headers = {'User-Agent':'Mozilla/5'})
	data = json.loads(request.urlopen(usdaUrl).read())
	nutrientInfo = data['foods'][0]['food']['nutrients']
	nutrientDict = {}
	for nutrient in nutrientInfo:
		nutrientDict[nutrient['name']] = nutrient['value'] + " " + nutrient['unit']
	return nutrientDict


print(getTypeDict("new","cities"))
print(getTypeDict("1","establishments"))
print(getTypeDict("1","cuisines"))
print(searchRestuarant("1","1","1"))
print("------------------------------------------------------")
print(searchIngredient("butter"))
print(getInfo("42148"))
print("------------------------------------------------------")
print(searchRecs("butter"))
print(getRecs("47050"))
print("------------------------------------------------------")
