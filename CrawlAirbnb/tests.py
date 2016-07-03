
from bs4 import BeautifulSoup
import requests
import json
import logging
import abn_parser
import abn_meta

logger = logging.getLogger('')# root logger
logger.setLevel(logging.DEBUG)

def pprint_json(text,outname):
    d = json.loads(text)
    with open(outname,"wt") as outfile:
        json.dump(d,outfile,indent=4)


meta = abn_meta.MetaInfo()
listing_id = 1246769
room = abn_parser.parse_room(listing_id,meta)
d = room.to_dict()
with open("temp3.json","wt") as outf:
    json.dump(d,outf,indent=4)


listing_id=1246769
url = "https://www.airbnb.com/rooms/{}".format(listing_id)
response = requests.get(url)
soup = BeautifulSoup(response.content)
tag = soup.find('script',{'type':"application/json",'data-hypernova-key':"listingbundlejs"})


with open(outname,"wt") as outfile:
    json.dump(d,outfile,indent=4)


listing_id = 1246769
url = "https://www.airbnb.com/rooms/{}".format(listing_id)
response = requests.get(url)
soup = BeautifulSoup(response.content)
    
tag = soup.find('script',{'type':"application/json",'data-hypernova-key':"listingbundlejs"})
# json text is embedded in '<!--xxx-->', so remove comment tags at both ends
d = json.loads( tag.text[4:-3] )

dict_listing = d["listing"]































