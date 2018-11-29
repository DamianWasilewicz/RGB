from urllib import request
import json

f2fKey = "50eb99e18a32f2eb95b721b09a2c4402"
zomatoKey = "50427fa83b5eda149411a00deb4cedc5"
yelpKey = "WZvWvogiVfxzNrpWipq63HV1fAJZKU4R-kDfewNhYQssKpX\
jFCbbdwe0IGQW7Bh86cEEL7Xh5Yb8bgGOfgYaCJQ5BXt2-n0v4ymnkdL49ou1Ot1vNDBI__0egaj0W3Yx"
usdaKey = "LSwsFBYAj6DAx8ChR6hy5420iIX8IyQCPoDMGt3G"


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

# print(getCites("new"))


# zomatoUrl = request.Request("https://developers.zomato.com/api/v2.1")
# cityString = "/cities?q="
# queryString = "/establishment/city_id=1"
# zomatoUrl.add_header("user-key", zomatoKey)
# zomatoUrl.add_header('User-Agent','Mozilla/5.0')
# data = json.loads(request.urlopen(zomatoUrl).read())
# print(data)
