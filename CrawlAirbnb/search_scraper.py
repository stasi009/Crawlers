﻿
import requests
import time
import logging

def _onepage_search(location,offset,limits=50):
    base_url = "https://api.airbnb.com/v2/search_results?client_id=3092nxybyb0otqw18e8nh5nty"
    search_parameters = {'location':location,'_offset':offset,'_limit':limits}
    
    response = requests.get(base_url,search_parameters)
    try:
        search_results = response.json()["search_results"]

        eof = True if len(search_results) < limits else False
        return eof,( result["listing"]["id"]  for result in search_results )
    except KeyError:
        logging.error("status_code=%d, content='%s'",response.status_code,response.text)

def search(location,offset,sleep_interval=1, limits=50):
    eof = False
    while not eof:
        eof, listingids = _onepage_search(location,offset,limits)

        for listingid in listingids:
            yield listingid

        offset += limits
        time.sleep(sleep_interval)

########################################
# location = "San-Francisco--CA"
location = "New-York--NY--United-States"
offset = 0
limits = 50

search_results_iterator = search(location,offset,sleep_interval=2)
for index,listingid in enumerate(search_results_iterator):
    print "[{}]: {}".format(index+1,listingid)


