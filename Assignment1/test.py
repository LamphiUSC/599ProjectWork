import geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim()
from geopy.exc import GeocoderTimedOut
location="Jamesville, MD"
geo_location = geolocator.geocode(location,timeout=10)
print geo_location