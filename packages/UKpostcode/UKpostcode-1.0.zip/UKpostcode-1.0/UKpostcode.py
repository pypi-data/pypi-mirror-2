"""
Look up UK postcodes using the API provided at uk-postcodes.com,
based on open data from the Ordnance Survey.

Simplest usage:
import UKpostcode
lat, long = UKpostcode.latlong("CB2 1RD")

More data:
geodata = UKpostcode.all_data("CB2 1RD")
(See the documentation for all_data)

This module does not implement any sort of caching.
"""

import urllib
import json
API = "http://www.uk-postcodes.com/postcode/"

"""
Returns all data available about the postcode:
'postcode' (display form)
'geo': ('lat', 'long', 'easting', 'northing', 'geohash' (a URL))
'administrative': ('county', 'district', 'ward' --for each, 'title' and 'uri' (a link to statistics.gov.uk)

Usage:
geodata = UKpostcode.alldata("CB2 1RD")
print geodata['administrative']['county']['title']
"""
def all_data(postcode):
	postcode = postcode.replace(" ","")
	uin = urllib.urlopen(API + postcode + ".json")
	return json.load(uin)
	
"""
Get the latitude and longitude from a postcode.

Usage:
lat, long = UKpostcode.latlong("CB2 1RD")
"""
def latlong(postcode):
	geodata = all_data(postcode)['geo']
	return float(geodata['lat']), float(geodata['lng'])
	
if __name__ == "__main__":
	print "CB2 1RD:", latlong("CB2 1RD")
