import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from models.database.database import Database
from models.database.locationData import LocationData

class Location:

    def __init__(self, city:str, country:str, id:int =-1):
        self.ID = id
        self.city = city
        self.country = country
        if self.ID ==-1 and not LocationData.is_unique(city, country):
            l = Location._get_unique(city, country)
            self.ID = l.ID
        elif self.ID == -1:
            self.save()
            l = Location._get_unique(city, country)
            self.ID = l.ID

    def save(self):
        LocationData.insert(self.city, self.country)

    def __repr__(self) -> str:
        return f"<Location: {self.ID}, {self.city} in {self.country}>"

    @classmethod
    def from_tuple(cls, t:tuple):
        return Location(t[1], t[2], t[0])
    
    @classmethod
    def from_id(cls, id:int):
        t = Database.get_by_unique_value(LocationData.TABLE_NAME, 'id', id)
        return Location.from_tuple(t)
    
    @classmethod
    def all(cls):
        t = Database.fetch_all(LocationData.TABLE_NAME)
        l =[]
        for b in t:
            l.append(Location.from_tuple(b))
        return l
    
    @classmethod
    def _get_unique(cls, city:str, country:str):
        return Location.from_tuple(LocationData.get_unique(city, country))
