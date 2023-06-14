import overpy
import requests
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="cinema_extraction")
location = geolocator.geocode("Waikato")
lat = location.latitude
lon = location.longitude


api = overpy.Overpass()


radius = 100000
# Define the query to fetch cinema nodes within a certain radius
query = f"""
node["amenity"="cinema"](around:{radius},{lat},{lon});
out;
"""

result = api.query(query)


cinemas = []
for node in result.nodes:
    cinema = {
        "name": node.tags.get("name", ""),
        "lat": node.lat,
        "lon": node.lon,
        "address": node.tags.get("addr:full", ""),
        "capacity": node.tags.get("capacity", "Unknown"),
    }
    print(cinema)
