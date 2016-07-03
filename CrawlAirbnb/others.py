
Aspects = ["Accuracy","Communication","Cleanliness","Location","Check In","Value"]
AspectPatterns = dict((aspect,re.compile(r'\${}.0.0.0$'.format(aspect))) for aspect in Aspects)

def get_aspect_rating(soup,aspect,listingid):
    pattern = AspectPatterns[aspect]
    tags = soup.findAll('div',{'class':'star-rating','data-reactid':pattern})
    if len(tags) == 1:
        return float(tags[0].attrs["content"])
    elif len(tags) == 0: # not found
        return None
    else:
        errmsg = "Room<{}> has {} ratings for '{}'".format(listingid,len(tags),aspect)
        raise Exception(errmsg)