
from bs4 import BeautifulSoup
import requests
import json
import logging
from abn_entities import Room
from listing_scraper import ListingScraper
from listing_saver import ListingJsonSaver
from meta_info import MetaInfo

logger = logging.getLogger('crawlabn')
logger.setLevel(logging.INFO)


meta = MetaInfo()
listing_scraper = ListingScraper(meta,None,None)

listing_id = 25002
room = listing_scraper.get_room(listing_id)

saver = ListingJsonSaver("rooms_json")
saver.save(room)



url = "https://api.airbnb.com/v2/reviews?client_id=3092nxybyb0otqw18e8nh5nty&listing_id=2056659&role=all&_limit=60"
r = requests.get(url)




































