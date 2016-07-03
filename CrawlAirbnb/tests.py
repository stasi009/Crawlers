
from bs4 import BeautifulSoup
import requests
import json
import logging
import abn_parser
import abn_meta

logger = logging.getLogger('')# root logger
logger.setLevel(logging.INFO)


meta = abn_meta.MetaInfo()
listing_id = 1246769
room = abn_parser.parse_room(listing_id,meta)
d = room.to_dict()
with open("temp3.json","wt") as outf:
    json.dump(d,outf,indent=4)


url = "https://api.airbnb.com/v2/search_results?client_id=3092nxybyb0otqw18e8nh5nty&locale=en-US&currency=USD&_format=for_search_results_with_minimal_pricing&_limit=10&_offset=0&fetch_facets=true&guests=1&ib=false&ib_add_photo_flow=true&location=Lake%20Tahoe%2C%20CA%2C%20US&min_bathrooms=0&min_bedrooms=0&min_beds=1&min_num_pic_urls=10&price_max=210&price_min=40&sort=1&user_lat=37.3398634&user_lng=-122.0455164"
response = requests.get(url)
pprint_json(response.text,"temp5.json")































