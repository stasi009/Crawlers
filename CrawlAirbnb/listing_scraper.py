

from bs4 import BeautifulSoup
import requests
import json
import re
import itertools
import threading
import time
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

class ListingScraper(threading.Thread):
    def __init__(self,meta,inQ,outQ,settings = {}):
        threading.Thread.__init__(self)
        self._meta = meta
        self._inQ = inQ
        self._outQ = outQ
        
        self._logger = logging.getLogger("crawlabn.listing")
        self._sleep_interval = settings.get("sleep_interval",2)# unit: seconds
        self._page_limits = settings.get("page_limits",50)# maximal size in a page

    def get_evaluations(self,room):
        response = requests.get("https://www.airbnb.com/rooms/{}".format(room.id))
        if response.ok:
            self._logger.info("listing<%d>'s webpage downloaded",room.id)

            soup = BeautifulSoup(response.text)
            tag = soup.find('script',{'type':"application/json",'data-hypernova-key':"listingbundlejs"})
            # json text is embedded in '<!--xxx-->', so remove comment tags at both ends
            d = json.loads( tag.text[4:-3] )

            ################ star distribution
            dict_star_histogram = d["starHistogramData"]
            for s in dict_star_histogram:
                r = int( s["rating"])
                # rating is from 1 to 5, so have to r-1
                room.star_percentages[r-1] = s["percentage"]

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
            self._logger.info("listing<%d>'s comments from [%d~%d] downloaded",listingid,offset,offset+limits)

            # if there is no reviews, response still have 'reviews' section, but just empty
            reviews = response.json()["reviews"]

            eof = True if len(reviews) < limits else False
            return eof,(review["comments"] for review in reviews if is_english(review["comments"]) )
        else:
            self._logger.error("failed to download listing<%d>'s comments from [%d~%d] downloaded, status code=%d, reason='%s', content='%s'",listingid,offset,offset+limits, response.status_code,response.reason,response.text)
            response.raise_for_status()

    def get_room(self,listing_id):
        #################### basic information
        time.sleep(self._sleep_interval)
        api_url = "https://api.airbnb.com/v2/listings/{}?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3".format(listing_id)
        response = requests.get(api_url)
        if response.ok:
            self._logger.info("JSON downloaded from listing<%d>'s API",listing_id)
            room = Room(response.json()["listing"])
        else:
            self._logger.error("failed to download listing<%d>'s from API, status code=%d, reason='%s', content='%s'",listingid,offset,offset+limits, response.status_code,response.reason,response.text)
            response.raise_for_status()

        #################### aspect ratings
        time.sleep(self._sleep_interval)
        self.get_evaluations(room)

        #################### comments
        offset = 0
        eof = False
        while not eof:
            time.sleep(self._sleep_interval)
            eof,comments = self.get_onepage_comments(room.id,offset,self._page_limits)
            room.comments.extend(comments)
            offset += self._page_limits

        return room










