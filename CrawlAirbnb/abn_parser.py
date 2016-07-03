

from bs4 import BeautifulSoup
import requests
import json
import re
import itertools
from abn_entities import Room

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

def parse_evaluations(room,meta):
    url = "https://www.airbnb.com/rooms/{}".format(room.id)
    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    
    tag = soup.find('script',{'type':"application/json",'data-hypernova-key':"listingbundlejs"})
    # json text is embedded in '<!--xxx-->', so remove comment tags at both ends
    d = json.loads( tag.text[4:-3] )

    ################ star distribution
    dict_star_histogram = d["starHistogramData"]
    for s in dict_star_histogram:
        r = int( s["rating"])
        # rating is from 1 to 5, so have to r-1
        room.star_distribution[r-1] = s["percentage"]

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
        room.review_tags.append(meta.tagid2txt(tagid))

    ################ how many save this room into their wishlist
    room.saved2wishlist = get_saved2wishlist(soup,room.id)

def is_english(txt):
    try:
        txt.decode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

def parse_comments(listingid):
    api_url = "https://api.airbnb.com/v2/reviews?client_id=3092nxybyb0otqw18e8nh5nty&listing_id={}&role=all".format(listingid)

    response = requests.get(api_url)
    # if there is no reviews, response still have 'reviews' section, but just empty
    reviews = response.json()["reviews"]

    return [review["comments"] for review in reviews if is_english(review["comments"])]

def parse_room(listing_id,meta):
    #################### basic information
    api_url = "https://api.airbnb.com/v2/listings/{}?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3".format(listing_id)
    response = requests.get(api_url)
    room = Room(response.json()["listing"])

    #################### aspect ratings
    parse_evaluations(room,meta)

    #################### comments
    room.comments = parse_comments(listing_id)

    return room



