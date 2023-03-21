import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from database.database import Database

class TagData:
    TABLE_NAME= 'tags'
    VALUE_NAMES =('name',)

    """Insert new tag. True on success, False if tag already exists."""
    @classmethod
    def insert(cls, name:str) -> bool:
        #Checks if there is already such a entry.
        if Database.query_fetch(f"SELECT * FROM {TagData.TABLE_NAME} WHERE name = ?;",
                                    (name,)):
            return False
        Database.unsafe_insert(TagData.TABLE_NAME, TagData.VALUE_NAMES, (name,))
        return True
    

    
class QuoteTagData:
    TABLE_NAME= 'quotes_tags'
    VALUE_NAMES =('quote_id', 'tag_id')

    @classmethod
    def insert(cls, quote_id:int, tag_id:int) -> bool:
        #Checks if there is already such a entry.
        if Database.query_fetch(f"SELECT * FROM {QuoteTagData.TABLE_NAME} WHERE quote_id = ? and tag_id = ?;",
                                    (quote_id, tag_id)):
            return False
        Database.unsafe_insert(QuoteTagData.TABLE_NAME, QuoteTagData.VALUE_NAMES, (quote_id, tag_id))
        return True
    