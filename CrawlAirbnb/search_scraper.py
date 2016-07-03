
import requests
import time
import logging
import threading

class SearchScraper(threading.Thread):

    def __init__(self,settings = {}):
        threading.Thread.__init__(self)
        self._sleep_interval = settings.get("sleep_interval",2)# unit: seconds
        self._page_limits = settings.get("page_limits",50)# maximal size in a page
        self._logger = logging.getLogger("crawlabn.search")

    def search_onepage(self,location,offset,limits):
        base_url = "https://api.airbnb.com/v2/search_results?client_id=3092nxybyb0otqw18e8nh5nty"
        search_parameters = {'location':location,'_offset':offset,'_limit':limits}
        response = requests.get(base_url,search_parameters)
        if response.ok:
            self._logger.info("location<%s>'s search result from [%d~%d]",location,offset,offset+limits)
            search_results = response.json()["search_results"]

            nextpage = False if len(search_results) < limits else True
            return nextpage,[ result["listing"]["id"]  for result in search_results ]
        else:
            self._logger.error("failed to download location<%s>'s search results from [%d~%d], status code=%d, reason='%s', content='%s'",location,offset,offset+limits, response.status_code,response.reason,response.text)
            return False,None








