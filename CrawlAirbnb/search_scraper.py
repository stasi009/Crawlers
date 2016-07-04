
import requests
import time
import logging
import threading

class SearchScrapeAgent(threading.Thread):

    def __init__(self,locations,outQ,control):
        threading.Thread.__init__(self)
        self.daemon = True
        self._locations = locations
        self._outQ = outQ
        self._control = control
        self._logger = logging.getLogger("crawlabn.search")

    def _search_onepage(self,location,offset,limits):
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

    def run(self):
        for location in self._locations:
            self._logger.info("begin search listings for '%s', ......",location)

            num_pages = 0
            offset = 0
            nextpage = True
            while nextpage:
                nextpage, listingids = self._search_onepage(location,offset,self._control.page_limits)

                # split whole listing-ids into smaller chunks, which may improve parallelism
                for chunk in self._control.split(listingids):
                    self._outQ.put(chunk)

                num_pages += 1
                if self._control.search_pages >0 and num_pages >= self._control.search_pages:
                    nextpage = False
                    self._logger.info("exceed required %d pages",self._control.search_pages)
                else:
                    offset += self._control.page_limits
                    self._control.sleep()

            self._logger.info("-------- finish search listings for '%s', totally %d pages --------",location,num_pages)











