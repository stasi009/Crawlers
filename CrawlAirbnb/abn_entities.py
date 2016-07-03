

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
        self.zipcode = d["zipcode"]# if outside USA, zipcode may not be integer
        self.neighborhood = d["neighborhood"]
        self.instant_bookable = d["instant_bookable"]

        # ---------------------- hosts
        self.host =  Host(d["primary_host"])

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
        
        # ---------------------- evaluations
        self.business_travel = d.get("is_business_travel_ready",False)
        self.star_rating = d.get("star_rating",None)
        self.reviews_count = d.get("reviews_count",0)

        self.review_score = d.get("review_score", 0)
        self.aspect_ratings = d.get("aspect_ratings", {})
        self.saved2wishlist = d.get("saved2wishlist", 0)
        self.comments = d.get("comments", [])
        self.review_tags = d.get("review_tags", [])
        self.star_percentages = d.get("star_percentages", [-1 for i in xrange(5)])

    def to_dict(self):
        return {
            "id": self.id,
            "name":self.name,
            "city": self.city,
            "state": self.state ,
            "zipcode":self.zipcode,
            "instant_bookable": self.instant_bookable,
            "primary_host": self.host.to_dict(),
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
            "is_business_travel_ready":self.business_travel,
            "star_rating": self.star_rating ,
            "reviews_count": self.reviews_count,
            "aspect_ratings":self.aspect_ratings,
            "saved2wishlist":self.saved2wishlist,
            "comments": self.comments,
            "review_score": self.review_score,
            "review_tags": self.review_tags,
            "star_percentages": self.star_percentages
            }



