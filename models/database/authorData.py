import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from database.database import Database

class AuthorData:
    TABLE_NAME = 'authors'
    VALUE_NAMES = ('name', 'birthplace', 'birthdate')

    """Insert new author. True on success, False if author's name is taken or locations_id does not exits."""
    @classmethod
    def insert(cls, name:str, birthplace_id:int, birthdate_timestamp:int) -> bool:
        #Checks if name is taken.
        if Database.query_fetch(f"SELECT * FROM {AuthorData.TABLE_NAME} WHERE name = ?;",
                                    (name,)):
            return False
        #Checks there is locations with given id
        if Database.is_unique_value_free('locations', 'id', birthplace_id):
            return False
        Database.unsafe_insert(AuthorData.TABLE_NAME, AuthorData.VALUE_NAMES, (name, birthplace_id, birthdate_timestamp))
        return True
    
