
from bs4 import BeautifulSoup
import requests
import json
import logging
from abn_entities import Room
from listing_scraper import ListingScraper
from listing_saver import ListingJsonSaver
from meta_info import MetaInfo

logger = logging.getLogger('')# root logger
logger.setLevel(logging.INFO)


meta = MetaInfo()
listing_scraper = ListingScraper(meta,None,None)

listing_id = 1485746
room = listing_scraper.get_room(listing_id)

saver = ListingJsonSaver("rooms_json")
saver.save(room)




































