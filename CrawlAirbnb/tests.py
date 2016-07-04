
from bs4 import BeautifulSoup
import requests
import json
import logging
from Queue import Queue
from listing_scraper import ListingScrapeAgent
from listing_saver import ListingSaveAgent
from search_scraper import SearchScrapeAgent
from meta_info import MetaInfo
from crawl_control import Control

# --------------------------- configure logging
logger = logging.getLogger('crawlabn')
logger.setLevel(logging.INFO)

cloghandler = logging.StreamHandler()
cloghandler.setLevel(logging.INFO)
logger.addHandler(cloghandler)

floghandler = logging.FileHandler('errors.log',mode='w')
floghandler.setLevel(logging.WARNING)
logger.addHandler(floghandler)

# --------------------------- prepare
control = Control(search_pages = 1)
meta = MetaInfo()

listing_id_queue = Queue()
rooms_queue = Queue()

locations = ['San-Francisco--CA']
search_agent = SearchScrapeAgent(locations,listing_id_queue,control)
listing_scrape_agent = ListingScrapeAgent(listing_id_queue,rooms_queue,meta,control)
save_agent = ListingSaveAgent(rooms_queue,control)

# --------------------------- start
search_agent.start()
listing_scrape_agent.start()
save_agent.start()

# --------------------------- block main from existing
_ = raw_input("Press any key to exist, ......")













































