import datetime
import requests
from urllib import quote
import json
from datetime import datetime
import fire

meta_weather_endpoint = "https://www.metaweather.com/api/"
location_api = "location/search/?query="
latlong_api = "location/search/?lattlong="
woeid_api = "location/"


def get_lat_long_by_place_name(place_name):
    url = meta_weather_endpoint + location_api + quote(place_name)
    place = requests.get(url)
    __check_resp_status(place)

    location = __safe_parse_json(place.text)

    for x in range(0, len(location)):

        if location[x]['title'].lower() == place_name.lower():
            lat_long = (location[x]['latt_long']).split(',')
            return lat_long[0], lat_long[1]
    print "%s Not Found in response %s" % (place_name, location)
    return None, None


def get_woeid_by_place_name(place_name):
    url = meta_weather_endpoint + location_api + quote(place_name)
    place = requests.get(url)
    __check_resp_status(place)

    location = __safe_parse_json(place.text)
    for x in range(0, len(location)):
        woeid = location[x]['woeid']
        if location[x]['title'].lower() == place_name.lower():
            return woeid
    print "%s Not Found in response %s" % (place_name, location)
    return None


def check_place_name_by_lat_long(latitude, longitude, expected):
    url = meta_weather_endpoint + latlong_api + quote(latitude+","+longitude)
    place = requests.get(url)
    __check_resp_status(place)

    location = __safe_parse_json(place.text)
    print "Checking %s %s returns %s" % (latitude, longitude, expected)
    assert location[0]["title"].lower() == expected.lower(), "Location returned: %s is not as expected: %s" % (location[0]["title"], expected)


def get_weather_by_woeid(woeid):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    url = meta_weather_endpoint + woeid_api + str(woeid)

    place = requests.get(url)
    __check_resp_status(place)
    details = __safe_parse_json(place.text)

    weather = details['consolidated_weather']
    for x in range(0, len(weather)):
        if weather[x]['applicable_date'] == today:
            print "%s Today's Weather in %s : " % (today, details['title'])
            print ("Weather State: %s" % weather[x]['weather_state_name'])
            print ("Wind Speed: %s" % weather[x]['wind_speed'])
            print ("Temperature: %s" % weather[x]['the_temp'])


def __safe_parse_json(message):
    try:
        return json.loads(message)
    except Exception as e:
        print "Error parsing json", str(e)
        return message


def __check_resp_status(response):
    if response.status_code != 200:
        raise OSError("Response " + str(response.status_code)
                  + ": " + response.text)


def __assert_equals(arg1, arg2):
    if arg1 != arg2:
        raise ValueError(str(arg1) + " Is not equal to " + str(arg2))


def main(place_name):
    latitude, longitude = get_lat_long_by_place_name(place_name)
    if latitude is not None:
        check_place_name_by_lat_long(latitude, longitude, place_name)
    woe_id = get_woeid_by_place_name(place_name)
    if woe_id is not None:
        get_weather_by_woeid(woe_id)


if __name__ == "__main__":
    """
        Usage:
        weather_check.py "San Diego"
    """

fire.Fire(main)
