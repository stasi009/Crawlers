
import random
import time

class Control(object):

    def __init__(self,**kwargs):
        self._min_sleep = kwargs.get("min_sleep",1)# unit: seconds
        self._max_sleep = kwargs.get("max_sleep",4)# unit: seconds
        self.page_limits = kwargs.get("page_limits",50)# maximal size in a page
        self._unit_size = kwargs.get("unit_size",25)
        self.save_folder = kwargs.get("save_folder","rooms_json")
        self.search_pages = kwargs.get("search_pages",-1)

    def sleep(self):
        time.sleep(random.uniform(self._min_sleep,self._max_sleep))
    
    def split(self,alist):
        return (alist[offset:offset+self._unit_size] for offset in xrange(0,len(alist),self._unit_size))
