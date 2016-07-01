

from bs4 import BeautifulSoup
import requests
import json
import re
import itertools
from abn_entities import Room

Aspects = ["Accuracy","Communication","Cleanliness","Location","Check In","Value"]
AspectPatterns = dict((aspect,re.compile(r'\${}.0.0.0$'.format(aspect))) for aspect in Aspects)

def get_aspect_rating(soup,aspect,listingid):
    pattern = AspectPatterns[aspect]
    tags = soup.findAll('div',{'class':'star-rating','data-reactid':pattern})
    if len(tags) == 1:
        return float(tags[0].attrs["content"])
    elif len(tags) == 0: # not found
        return None
    else:
        errmsg = "Room<{}> has {} ratings for '{}'".format(listingid,len(tags),aspect)
        raise Exception(errmsg)

def get_saved2wishlist(soup,listingid):
    tags = soup.findAll('div',{'class':'wish_list_button'})
    if len(tags) == 1:
        return int(tags[0].attrs['data-count'])
    elif len(tags) == 0: # not found
        return None
    else:
        errmsg = "Room<{}> has {} 'saved to wishlist'".format(listingid,len(tags))
        raise Exception(errmsg)

def parse_aspect_ratings(room):
    url = "https://www.airbnb.com/rooms/{}".format(room.id)
    response = requests.get(url)
    soup = BeautifulSoup(response.content)

    room.aspect_ratings = dict((aspect, get_aspect_rating(soup,aspect,room.id))  for aspect in Aspects)
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
    reviews = json.loads(response.content)["reviews"]

    return [review["comments"] for review in reviews if is_english(review["comments"])]

def parse_room(listing_id):
    #################### basic information
    api_url = "https://api.airbnb.com/v2/listings/{}?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3".format(listing_id)
    response = requests.get(api_url)
    dict_room = json.loads(response.content)
    room = Room(dict_room["listing"])

    #################### aspect ratings
    parse_aspect_ratings(room)

    #################### comments
    room.comments = parse_comments(listing_id)

    return room



