
import json
import os
import logging
import threading

class ListingJsonSaver(object):

    def __init__(self,folder):
        self._folder = folder
        
    def save(self,room):
        fname = "{}_{}_{}.json".format(room.state,room.city,room.id)
        with open(os.path.join(self._folder, fname),"wt") as outfile:
            json.dump(room.to_dict(),outfile,indent=4)

class ListingSaveAgent(threading.Thread):

    def __init__(self,inQ,control):
        threading.Thread.__init__(self)
        self.daemon = True

        self._saver = ListingJsonSaver(control.save_folder)
        self._inQ = inQ
        self._logger = logging.getLogger("crawlabn.save")

    def run(self):
        while True:
            rooms = self._inQ.get()

            for room in rooms:
                self._saver.save(room)
                self._logger.info("listing<%d> '%s' saved",room.id,room.name)

            self._inQ.task_done()




