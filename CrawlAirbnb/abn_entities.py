

class Host(object):

    def __init__(self,d):
        self.id = d["id"]
        self.first_name = d["first_name"]
        self.is_superhost = d["is_superhost"]
        self.reviewee_count = d["reviewee_count"]

    def to_dict(self):
        return {"id":self.id,
                "first_name":self.first_name,
                "is_superhost":self.is_superhost,
                "reviewee_count":self.reviewee_count}

class Room(object):
    def __init__(self,d):
        # ---------------------- basic information
        self.id = d["id"]
        self.name = d["name"]
        self.city = d["city"]
        self.state = d["state"]
        self.neighborhood = d["neighborhood"]

        # ---------------------- space
        self.property_type = d["property_type"]
        self.room_type = d["room_type"]
        self.guests_included = d["guests_included"]
        self.bathrooms = d["bathrooms"]
        self.bedrooms = d["bedrooms"]
        self.beds = d["beds"]
        
        # ---------------------- description
        self.summary = d.get("summary","")
        self.space = d.get("space","")
        self.guest_access = d.get("access","")
        self.neighborhood_overview = d.get("neighborhood_overview","")
        self.transit = d.get("transit","")
        
        # ---------------------- price
        self.price_per_night = d["price"]
        self.month_price_factor = d["monthly_price_factor"]
        self.week_price_factor = d["weekly_price_factor"]
        
        # ---------------------- ratings
        self.rating = d.get("star_rating",None)
        self.reviews_count = d.get("reviews_count",0)

    def to_dict(self):
        d = {
            "id": self.id,
            "name":self.name,
            "city": self.city,
            "state": self.state ,
            "neighborhood": self.neighborhood,
            "property_type": self.property_type, 
            "room_type": self.room_type,
            "guests_included": self.guests_included,
            "bathrooms": self.bathrooms,
            "bedrooms": self.bedrooms,
            "beds": self.beds,
            "summary": self.summary,
            "space": self.space ,
            "access": self.guest_access,
            "neighborhood_overview": self.neighborhood_overview,
            "transit": self.transit,
            "price": self.price_per_night ,
            "monthly_price_factor": self.month_price_factor,
            "weekly_price_factor": self.week_price_factor,
            "star_rating": self.rating ,
            "reviews_count": self.reviews_count,
            }

        try:
            d["aspect_ratings"] = self.aspect_ratings
        except AttributeError:
            pass

        try:
            d["saved2wishlist"] = self.saved2wishlist
        except AttributeError:
            pass

        try:
            d["comments"] = self.comments
        except AttributeError:
            pass

        return d



