
from bs4 import BeautifulSoup
import requests
import json
import abn_parser

def pprint_json(text,outname):
    d = json.loads(text)
    with open(outname,"wt") as outfile:
        json.dump(d,outfile,indent=4)



listing_id = 10705179
room = abn_parser.parse_room(listing_id)
d = room.to_dict()

with open("temp3.json","wt") as outf:
    json.dump(d,outf,indent=4)




