import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from database.database import Database

class QuoteData:
    TABLE_NAME= 'quotes'
    VALUE_NAMES = ('author_id', 'quote')

    """Insert new quote. True on success, False if quote is already in db or author's id does not exits."""
    @classmethod
    def insert(cls, author_id:int, quote:str) -> bool:
        #Checks if quote is already in db
        if Database.query_fetch(f"SELECT * FROM {QuoteData.TABLE_NAME} WHERE quote = ?;",
                                    (quote,)):
            return False
        #Checks there is author with given id
        if Database.is_unique_value_free('authors', 'id', author_id):
            return False
        Database.unsafe_insert(QuoteData.TABLE_NAME, QuoteData.VALUE_NAMES, (author_id, quote))
        return True
