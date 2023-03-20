from database import Database

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
