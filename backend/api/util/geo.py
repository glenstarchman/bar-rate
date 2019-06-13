import re
import math
from django.conf import settings
import inflection
import requests
from pygeocoder import Geocoder
import geocoder
from django.contrib.gis.geos import Point
import time

bearings = [0, 90, 180, 270]
geo = Geocoder(api_key=settings.GOOGLE_API_KEY)

# Distances are measured in miles.
# Longitudes and latitudes are measured in degrees.
# Earth is assumed to be perfectly spherical.

earth_radius = 3960.0
degrees_to_radians = math.pi/180.0
radians_to_degrees = 180.0/math.pi

def change_in_latitude(miles):
    "Given a distance north, return the change in latitude."
    return (miles/earth_radius)*radians_to_degrees

def change_in_longitude(latitude, miles):
    "Given a latitude and a distance west, return the change in longitude."
    # Find the radius of a circle around the earth at given latitude.
    r = earth_radius*math.cos(latitude*degrees_to_radians)
    return (miles/r)*radians_to_degrees


def normalize_city(city):
    city = inflection.titleize(city)
    c = re.sub(' +', ' ', city).strip()
    parts = ''
    if ',' in c:
        parts = list(map(lambda x: x.strip(), c.split(',')))
    else:
        parts = (city, '')

    if len(parts) > 0 and len(parts[-1]) == 2:
        parts[-1] = parts[-1].upper()

    return parts


def normalize_city_str(city):
    return ', '.join(normalize_city(city))


def get_loc_center(location):
    return geo.geocode(location).coordinates


def get_loc_from_address(address, count=0):
    # check location table first
    #matches = Location.objects.filter(city=normalize_city_str(address))
    #if matches.count() > 0:
    #    match = matches[0]
    #    return Point(float(match.lng), float(match.lat))

    # we attempt up to 5 times to get the geocoded address
    if count == 5:
        return Point(0, 0)

    try:
        loc = geocoder.google(address)
        lat, lng = loc.latlng
        # store for later
        n = normalize_city_str(address)
        p = Point(lng, lat)
        #Location.objects.create(city=n, lat=lat, lng=lng, location=p)
        return Point(float(lng), float(lat))
    except Exception as e:
        time.sleep(1)
        count += 1
        return get_loc_from_address(address, count)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_loc(ip):
    #matches = Location.objects.filter(ip=ip)
    if matches.count() > 0 and matches[0].city:
        match = matches[0]
        c = normalize_city(match.city)
        return {
            "latitude": match.lat,
            "longitude": match.lon,
            "city": c[0],
            "region": c[1]
        }

    freegeoip = "http://api.ipstack.com/%s?access_key=e335a3316f7ab9d4f802d32fd483c17b" % (ip)
    geo_r = requests.get(freegeoip)
    geo_json = geo_r.json()
    # store for future use
    #raise(Exception(str(geo_json)))
    p = Point(geo_json["longitude"], geo_json["latitude"])
    Location.objects.create(ip=ip, lat=geo_json["latitude"],
                            lng=geo_json["longitude"],
                            location=p)
    return geo_json


def get_city(request):
    ip = get_client_ip(request)
    loc = get_loc(ip)
    if not loc["city"]:
        loc["city"] = "Sacramento"
    if not loc["region_code"]:
        loc["region_code"] = "CA"
    return "%s, %s" % (loc["city"], loc["region_code"])


def _extract(g, key, default=''):
    a = g.get(key, {})
    return g.get(key, {}).get('short_name', '')


def normalize_address(address):
    a = geocoder.google(address)
    g = a.geojson['features'][0]['properties']['raw']
    street_number = _extract(g, 'street_number')
    street = _extract(g, 'route')
    subpremise = _extract(g, 'subpremise', None)
    city = _extract(g, 'locality')
    state = _extract(g, 'administrative_area_level_1')
    zipcode = _extract(g, 'postal_code')
    street_address1 = '%s %s' % (street_number, street)
    #street_address2 = subpremise

    return {
        'street_address1': street_address1,
        #'street_address2': street_address2,
        'city': city,
        'state': state,
        'zipcode': zipcode

    }
