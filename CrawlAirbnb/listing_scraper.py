

from bs4 import BeautifulSoup
import requests
import json
import re
import itertools
import threading
import logging
from abn_entities import Room

def is_english(txt):
    try:
        txt.decode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

def get_saved2wishlist(soup,listingid):
    tags = soup.findAll('div',{'class':'wish_list_button'})
    if len(tags) == 1:
        return int(tags[0].attrs['data-count'])
    elif len(tags) == 0: # not found
        return 0
    else:
        errmsg = "Room<{}> has {} 'saved to wishlist'".format(listingid,len(tags))
        raise Exception(errmsg)

def get_review_tags(soup,meta):
    tag = soup.find('script',{'type':"application/json",'data-hypernova-key':"listingbundlejs"})
    if tag is None:
        return []
    else:
        return None

class ListingScraper(object):
    def __init__(self,meta,control,logger):
        self._meta = meta
        self._control = control
        self._logger = logger

    def get_evaluations(self,room):
        response = requests.get("https://www.airbnb.com/rooms/{}".format(room.id))
        if response.ok:
            self._logger.info("listing<%d>'s webpage downloaded to get evaluations",room.id)

            soup = BeautifulSoup(response.text)
            tag = soup.find('script',{'type':"application/json",'data-hypernova-key':"listingbundlejs"})
            # json text is embedded in '<!--xxx-->', so remove comment tags at
            # both ends
            d = json.loads(tag.text[4:-3])

            ################ star distribution
            dict_star_histogram = d["starHistogramData"]
            for s in dict_star_histogram:
                r = int(s["rating"])
                # rating is from 1 to 5, so have to r-1
                room.star_percentages[r - 1] = s["percentage"]

            dict_listing = d["listing"]
            ################ retrieve aspect ratings
            room.review_score = dict_listing["review_details_interface"]["review_score"]

            review_summary = dict_listing["review_details_interface"]["review_summary"]
            for aspect in review_summary:
                room.aspect_ratings[aspect["label"]] = aspect["value"] 

            ################ retrieve review tags
            review_tags = dict_listing["listing_tags"]
            for tag in review_tags:
                tagid = tag["tagId"]
                # order is important, only show first 5 on the page
                # so the first 5 must be the most important 5 aspects
                room.review_tags.append(self._meta.tagid2txt(tagid))

            ################ how many save this room into their wishlist
            room.saved2wishlist = get_saved2wishlist(soup,room.id)
        else:
            self._logger.error("failed to download listing<%d>'s webpage, status code=%d, reason='%s', content='%s'",room.id, response.status_code,response.reason,response.text)
            response.raise_for_status()

    def get_onepage_comments(self,listingid,offset,limits=50):
        api_url = "https://api.airbnb.com/v2/reviews?client_id=3092nxybyb0otqw18e8nh5nty&role=all&listing_id={}&_offset={}&_limit={}".format(listingid,offset,limits)
        response = requests.get(api_url)

        if response.ok:
            self._logger.info("listing<%d>'s comments from [%d~%d] downloaded",listingid,offset,offset + limits)

            # if there is no reviews, response still have 'reviews' section,
            # but just empty
            reviews = response.json()["reviews"]

            nextpage = False if len(reviews) < limits else True
            return nextpage,(review["comments"] for review in reviews if is_english(review["comments"]) )
        else:
            self._logger.error("failed to download listing<%d>'s comments from [%d~%d], status code=%d, reason='%s', content='%s'",listingid,offset,offset + limits, response.status_code,response.reason,response.text)
            return False,None # stop when error occurs

    def get_room(self,listing_id):
        #################### basic information
        self._control.sleep()
        api_url = "https://api.airbnb.com/v2/listings/{}?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3".format(listing_id)
        response = requests.get(api_url)
        if response.ok:
            self._logger.info("basic informations downloaded from listing<%d>'s API",listing_id)
            room = Room(response.json()["listing"])
        else:
            self._logger.error("failed to download listing<%d>'s from API, status code=%d, reason='%s', content='%s'",listing_id, response.status_code,response.reason,response.text)
            response.raise_for_status()

        #################### aspect ratings
        self._control.sleep()
        self.get_evaluations(room)

        #################### comments
        offset = 0
        nextpage = True
        while nextpage:
            self._control.sleep()
            nextpage,comments = self.get_onepage_comments(room.id,offset,self._control.page_limits)
            room.comments.extend(comments)
            offset += self._control.page_limits

        self._logger.info("completes scraping listing<%d>",listing_id)
        return room

class ListingScrapeAgent(threading.Thread):

    def __init__(self,inQ,outQ,meta,control):
        threading.Thread.__init__(self)
        self.daemon = True
        self._inQ = inQ
        self._outQ = outQ
        self._logger = logging.getLogger("crawlabn.listing")
        self._scraper = ListingScraper(meta,control,self._logger)

    def run(self):
        while True:
            listingids = self._inQ.get()

            rooms = []
            for listingid in listingids:
                try:
                    room = self._scraper.get_room(listingid)
                    rooms.append(room)
                except Exception as error:
                    self._logger.error("failed to scrape listing<%d> due to '%s'",listingid,str(error))

            if len(rooms) > 0:
                self._outQ.put(rooms)
                self._logger.info("########### scraped %d rooms ###########",len(rooms))

            self._inQ.task_done()












