from urllib import request
import json

try:
    with open('api.json', 'r') as file:
        api_dict = json.load(file)
except:
    print("Missing api.json")

def getTypeDict(query, type):
    """Return the dictionary based on the type specified {name of type:zomato specific id}.
    The dictionary depends on the type given: cities, establishments or cuisines.
    """
    try:
        query = query.strip()
        typeDict = dict() #creates a dictionary of type
        if (type == "cities"):
            query = query.replace(" ", "_")
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
    except:
        return None

def searchRestuarant(city, establishment, cuisine):
    """Return 10 restuarants that fall into the criteria of city, establishment and cuisine.
    Single restuarant list is [name, address, location]
    """
    try:
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
    except:
        return None

def searchRecs(ingredients):
    """Return a dictionary of at most 30 top available recipes and id given a list of ingredients"""
    try:
        ingredients = ingredients.strip().replace(" ", "%20")
        f2fUrl =  request.Request("https://www.food2fork.com/api/search?key=" + api_dict["f2f"] + "&q=" + ingredients, headers={'User-Agent': 'Mozilla/5.0'})
        data = json.loads(request.urlopen(f2fUrl).read())
        listOfRecs = data['recipes']
        recs = {}
        for rec in listOfRecs:
            recs[rec['title']] = rec['recipe_id']
        return recs
    except:
        return None

def getRecs(rec_id):
    """Return a list of data regarding the recipe: [name, ingredients, source, image] given a recipe id from the F2F database."""
    try:
        f2fUrl =  request.Request("https://www.food2fork.com/api/get?key=" + api_dict["f2f"] + "&rId=" + rec_id, headers={'User-Agent': 'Mozilla/5.0'})
        data = json.loads(request.urlopen(f2fUrl).read())
        return [data['recipe']['title'], data['recipe']['ingredients'], data['recipe']['source_url'], data['recipe']['image_url'],rec_id]
    except:
        return None

def searchIngredient(ingredient):
    """Return a dictionary of at most 20 top results when searched for that ingredient paired with ndbno (USDA id) given an ingredient."""
    try:
        ingredient = ingredient.strip().replace(" ", "%20")
        usdaUrl = request.Request("https://api.nal.usda.gov/ndb/search/?format=json&sort=r&max=20&offset=0&ds=Standard%20Reference" + "&q=" + ingredient + "&api_key=" + api_dict["usda"], headers={'User-Agent': 'Mozilla/5.0'})
        #usdaUrl.add_header("q", ingredient)
        #usdaUrl.add_header("api_key", api_dict["usda"])
        #usdaUrl.add_header('User-Agent','Mozilla/5.0')
        data = json.loads(request.urlopen(usdaUrl).read())
        listOfIng = data['list']['item']
        ingreds = {}
        for ing in listOfIng:
            ingreds[ing['name']] = ing['ndbno']
        # print(ingreds)
        return ingreds
    except:
        return None

def getInfo(ndbno):
    """Return a dictionary with nutrient {name : nutrient value} given a valid ndbno id."""
    try:
        usdaUrl = request.Request("https://api.nal.usda.gov/ndb/V2/reports?type=b&format=json&" + "ndbno=" + ndbno + "&api_key=" + api_dict['usda'],  headers = {'User-Agent':'Mozilla/5'})
        data = json.loads(request.urlopen(usdaUrl).read())
        nutrientInfo = data['foods'][0]['food']['nutrients']
        nutrientDict = {}
        for nutrient in nutrientInfo:
            nutrientDict[nutrient['name']] = nutrient['value'] + " " + nutrient['unit']
        return nutrientDict
    except:
        return None


# print(getTypeDict("new","cities"))
# print(getTypeDict("1","establishments"))
# print(getTypeDict("1","cuisines"))
# print(searchRestuarant("1","1","1"))
# print("------------------------------------------------------")
# print(searchIngredient("butter"))
# print(getInfo("42148"))
# print("------------------------------------------------------")
# print(searchRecs("butter"))
# print(getRecs("47050"))
# print("------------------------------------------------------")
