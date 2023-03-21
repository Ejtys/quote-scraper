import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from database.database import Database
from database.quoteData import QuoteData

from models.authorModel import Author


class Quote:

    def __init__(self, author:Author, quote:str, id:int = -1):
        self.ID = id
        
        if isinstance(author, int):
            self.author = Author.from_id(author)
        elif isinstance(author, str):
            self.author = Author.from_name(author)
        else:
            self.author = author
        
        if not isinstance(self.author, Author):
            raise ValueError("Not proper value for Author. Pass Author obj. If you are sure author exists in db you can pass id or name.")
        
        self.quote = quote

        if self.ID == -1 and not Quote.from_quote(quote):
            self.save()
            self.ID = Quote.from_quote(quote).ID
        elif self.ID == -1 and Quote.from_quote(quote):
            self.ID = q = Quote.from_quote(quote).ID


    def save(self):
        QuoteData.insert(self.author.ID, self.quote)

    def __repr__(self) -> str:
        return f"<Quote {self.ID}: \"{self.quote}\" by {self.author.name}>"

    @classmethod
    def from_tuple(cls, t:tuple):
        return Quote(t[1], t[2], t[0])
    
    @classmethod
    def from_id(cls, id:int):
        t = Database.get_by_unique_value(QuoteData.TABLE_NAME, 'id', id)
        if t:
            return Quote.from_tuple(t)
    
    @classmethod
    def from_quote(cls, quote:str):
        t = Database.get_by_unique_value(QuoteData.TABLE_NAME, 'quote', quote)
        if t:
            return Quote.from_tuple(t)

    @classmethod
    def all(cls):
        t = Database.fetch_all(QuoteData.TABLE_NAME)
        l =[]
        for b in t:
            l.append(Quote.from_tuple(b))
        return l
    
