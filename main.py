import sys
import requests

from Samples.business import find_businesses
from Samples.distance import lonlat_distance
from Samples.geocoder import get_coordinates
from Samples.mapapi_PG import show_map


coords = '37.90374,59.11963'

show_map(add_params=f'll={coords}&spn=0.02,0.02')

