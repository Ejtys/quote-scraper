import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from database.database import Database

class LocationData:
    TABLE_NAME = 'locations'
    VALUE_NAMES =('city', 'country')

    """Insert new location. True on success, False if location already exists."""
    @classmethod
    def insert(cls, city:str, country:str) -> bool:
        #Checks if there is already such a entry.
        if Database.query_fetch(f"SELECT * FROM {LocationData.TABLE_NAME} WHERE city = ? and country = ?;",
                                    (city, country)):
            return False
        Database.unsafe_insert(LocationData.TABLE_NAME, LocationData.VALUE_NAMES, (city, country))
        return True

    @classmethod
    def get_unique(cls, city:str, country:str):
        return Database.query_fetch(f"SELECT * FROM {LocationData.TABLE_NAME} WHERE city = ? and country = ?;",
                                    (city, country))[0]
    
    @classmethod
    def is_unique(cls, city:str, country:str):
        return not Database.query_fetch(f"SELECT * FROM {LocationData.TABLE_NAME} WHERE city = ? and country = ?;",
                                    (city, country))