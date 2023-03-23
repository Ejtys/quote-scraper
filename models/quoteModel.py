import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from models.database.database import Database
from models.database.quoteData import QuoteData
from models.database.tagData import TagData
from models.database.tagData import QuoteTagData

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
            raise ValueError(f"Author object expected")
        
        self.quote = quote

        if self.ID == -1 and not Quote.from_quote(quote):
            self.save()
            self.ID = Quote.from_quote(quote).ID
        elif self.ID == -1 and Quote.from_quote(quote):
            self.ID = q = Quote.from_quote(quote).ID


    def save(self):
        QuoteData.insert(self.author.ID, self.quote)

    def add_tag(self, tag:str):
        t = Tag(tag)
        t.connect(self.ID)

    @property
    def tags(self) -> list:
        return [Tag.from_id(x)for x in QuoteTagData.get_tags_for_quote(self.ID)]

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
    

class Tag:

    def __init__(self, name:str, id:int = -1):
        self.ID = id
        self.name = name

        if self.ID == -1 and Tag.from_name(name):
            self.ID = Tag.from_name(name).ID
        elif self.ID == -1:
            self.save()
            self.ID = Tag.from_name(name).ID

    def save(self):
        TagData.insert(self.name)

    def __repr__(self) -> str:
        return f'<Tag {self.ID}: {self.name}>'
    
    def connect(self, quote_id:int):
        QuoteTagData.insert(quote_id, self.ID)

    @property
    def quotes(self) -> list:
        return [Quote.from_id(x) for x in QuoteTagData.get_quotes_for_tag(self.ID)]

    @classmethod
    def from_id(cls, id:int):
        t = Database.get_by_unique_value(TagData.TABLE_NAME, 'id', id)
        if t:
            return Tag(t[1], t[0])
        
    @classmethod
    def from_name(cls, name:str):
        t = Database.get_by_unique_value(TagData.TABLE_NAME, 'name', name)
        if t:
            return Tag(t[1], t[0])
        
    @classmethod
    def all(cls):
        t = Database.fetch_all(TagData.TABLE_NAME)
        l = []
        for x in t:
            l.append(Tag(x[1], x[0]))
        return l

