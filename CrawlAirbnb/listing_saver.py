
import json
import os
import logging

class ListingJsonSaver(object):

    def __init__(self,folder):
        self._folder = folder
        self._logger = logging.getLogger("crawlabn.save")

    def save(self,room):
        fname = "{}_{}_{}.json".format(room.state,room.city,room.id)
        with open( os.path.join(self._folder, fname),"wt") as outfile:
            json.dump(room.to_dict(),outfile,indent=4)
        self._logger.info('[{}] saved'.format(fname))



