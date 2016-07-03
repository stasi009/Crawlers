
from bs4 import BeautifulSoup
import requests
import json
import logging
import abn_parser
import abn_meta

logger = logging.getLogger('')# root logger
logger.setLevel(logging.INFO)

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


url = "https://api.airbnb.com/v2/listings/1246769?client_id=3092nxybyb0otqw18e8nh5nty&_format=v1_legacy_for_p3"
response = requests.get(url)
pprint_json(response.content,"temp5.json")































