from urllib import request
import json

f2fKey = "50eb99e18a32f2eb95b721b09a2c4402"
zomatoKey = "50427fa83b5eda149411a00deb4cedc5"
yelpKey = "WZvWvogiVfxzNrpWipq63HV1fAJZKU4R-kDfewNhYQssKpX\
jFCbbdwe0IGQW7Bh86cEEL7Xh5Yb8bgGOfgYaCJQ5BXt2-n0v4ymnkdL49ou1Ot1vNDBI__0egaj0W3Yx"
usdaKey = "LSwsFBYAj6DAx8ChR6hy5420iIX8IyQCPoDMGt3G"


with open('api.json', 'r') as file:
    api_dict = json.load(file)


#returns a dictionary of city names with their ids
def getCites(city):
	cityDict = dict()
	cityString = "/cities?q=" + city
	zomatoUrl = request.Request("https://developers.zomato.com/api/v2.1" + cityString)
	zomatoUrl.add_header("user-key", zomatoKey)
	zomatoUrl.add_header('User-Agent','Mozilla/5.0')
	data = json.loads(request.urlopen(zomatoUrl).read())
	for cityList in data["location_suggestions"]:
		cityDict[cityList["name"]] = cityList["id"]
	return cityDict

'''
given a list of ingredients
returns a dictionary of at most 30 top available recipes and id
'''
def searchRecs(ingredients):
	query = ""
	for food in ingredients:
		query += food + ","
	print(query)
	f2fUrl =  request.Request("https://www.food2fork.com/api/search?key=" + f2fKey + "&q=" + query, headers={'User-Agent': 'Mozilla/5.0'})
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
    f2fUrl =  request.Request("https://www.food2fork.com/api/get?key=" + f2fKey + "&rId=" + rec_id, headers={'User-Agent': 'Mozilla/5.0'})
    data = json.loads(request.urlopen(f2fUrl).read())
    thing = [data['recipe']['ingredients'],data['recipe']['source_url']]
    return thing
	
'''
given an ingredient
returns a dictionary of at most 20 top results when searched for that ingredient paired with ndbno (USDA id)
'''
def searchIng(ingredient):
	usdaUrl = request.Request("https://api.nal.usda.gov/ndb/search/?format=json&sort=n&max=20&offset=0&ds=Standard%20Reference" + "&q=" + ingredient + "&api_key=" + api_dict["usda"], headers={'User-Agent': 'Mozilla/5.0'})
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
returns a dictionary with nutrient name : nutrient value
'''	
def getInfo(ndbno):
	usdaUrl = request.Request("https://api.nal.usda.gov/ndb/V2/reports?type=b&format=json&" + "ndbno=" + ndbno + "&api_key=" + api_dict['usda'],  headers = {'User-Agent':'Mozilla/5'})
	data = json.loads(request.urlopen(usdaUrl).read())
	nutsInfo = data['foods'][0]['food']['nutrients']
	nuts = {}
	for nutrient in nutsInfo:
		nuts[nutrient['name']] = nutrient['value'] + " " + nutrient['unit']
	return nuts
	
	
#li = ["grape%20juice"]
#print(searchRecs(li))
#print("------------------------------------------------------")
#print(getRecs("47050"))
#print("------------------------------------------------------")
#print("------------------------------------------------------")
print(searchIng("butter"))
print("------------------------------------------------------")
print(getInfo("42148"))
# print(getCites("new"))


# zomatoUrl = request.Request("https://developers.zomato.com/api/v2.1")
# cityString = "/cities?q="
# queryString = "/establishment/city_id=1"
# zomatoUrl.add_header("user-key", zomatoKey)
# zomatoUrl.add_header('User-Agent','Mozilla/5.0')
# data = json.loads(request.urlopen(zomatoUrl).read())
# print(data)
