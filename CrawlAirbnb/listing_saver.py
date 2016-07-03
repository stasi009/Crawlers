
import json
import os

class ListingJsonSaver(object):

    def __init__(self,folder):
        self._folder = folder

    def save(self,room):
        fname =  os.path.join(self._folder, "{}_{}.json".format(room.city,room.id))
        with open(fname,"wt") as outfile:
            json.dump(room.to_dict(),outfile,indent=4)

