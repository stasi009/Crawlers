
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import json
import requests
import logging

class MetaInfo(object):
    """
    retrieve some meta-information which is shared by all listings
    only retrieve once, after 1st retrival, keep these read-only information for later query
    """
    def __init__(self,seed_listingids = [10705179,1246769]):
        reviewtag_pattern = re.compile(r'review_tags.tag.\w+')
        self.__tags_id2txt = {}
        self._logger = logging.getLogger("crawlabn.meta")

        for candidate_id in seed_listingids:
            try:
                self._logger.info("try to load meta-info from listing<%d>, ......",candidate_id)
                url = "https://www.airbnb.com/rooms/{}".format(candidate_id)
                response = requests.get(url)
                soup = BeautifulSoup(response.text)

                tag = soup.find('meta',{'id':'_bootstrap-phrases'})
                if tag is None:
                    continue# try next listing
                else:
                    # we have to keep the order, so have to use 'OrderedDict'
                    d = json.loads(tag.attrs["content"], object_pairs_hook=OrderedDict)

                    counter = 0
                    for k,v in d.viewitems():
                        matched = reviewtag_pattern.match(k)
                        if matched is not None:
                            counter += 1
                            self.__tags_id2txt[counter] = v

                    self._logger.info("successfully load meta-info from listing<%d>",candidate_id)
                    break# stop after 1st successful loading
                    
            except Exception:
                self._logger.warning("failed to load meta-info from listing<%d>, try next", candidate_id)
                continue# try next listing

        # throw error if failed on all seed listings
        if len(self.__tags_id2txt) == 0:
            raise Exception("Cannot load meta-info from all seed listings")

    def tagid2txt(self,tagid):
        return self.__tags_id2txt[tagid]


