
from bs4 import BeautifulSoup
import requests
import json
import logging
from abn_entities import Room
from listing_scraper import ListingScraper
from listing_saver import ListingJsonSaver
from search_scraper import SearchScraper
from meta_info import MetaInfo

logger = logging.getLogger('crawlabn')
logger.setLevel(logging.INFO)

cloghandler = logging.StreamHandler()
cloghandler.setLevel(logging.INFO)
logger.addHandler(cloghandler)

floghandler = logging.FileHandler('errors.log',mode='w')
floghandler.setLevel(logging.WARNING)
logger.addHandler(floghandler)

meta = MetaInfo()
listing_scraper = ListingScraper(meta,None,None)

listing_id = 1308841
room = listing_scraper.get_room(listing_id)

saver = ListingJsonSaver("rooms_json")
saver.save(room)


searcher = SearchScraper()
nextpage,listingids = searcher.search_onepage("New-York--NY--United-States",1000,50)
if nextpage:
    print listingids
else:
    print "EOF"








































