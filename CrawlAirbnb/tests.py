
from bs4 import BeautifulSoup
import requests
import json
import abn_parser



listing_id = 12133747
room = abn_parser.parse_room(listing_id)
d = room.to_dict()

with open("temp3.json","wt") as outf:
    json.dump(d,outf,indent=4)















