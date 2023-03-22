import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from datetime import datetime

from database.database import Database
from database.authorData import AuthorData

from models.locationModel import Location


class Author:

    def __init__(self, name:str, birthplace:Location, birth_timestamp:int, id:int = -1):
        self.ID = id
        self.name = name
        if isinstance(birth_timestamp, str):
            self.birth_timestamp = Author.str_to_timestamp(birth_timestamp)
        else:
            self.birth_timestamp = birth_timestamp
        if isinstance(birthplace, int):
            self.birthplace = Location.from_id(birthplace)
        else:
             self.birthplace = birthplace
        if self.ID == -1 and not Author.from_name(self.name):
            self.save()
            self.ID = Author.from_name(self.name).ID
        if self.ID == -1:
            a = Author.from_name(self.name)
            self.ID = a.ID
            self.birth_timestamp = a.birth_timestamp
            self.birthplace = a.birthplace

    def save(self):
        AuthorData.insert(self.name, self.birthplace.ID, self.birth_timestamp)

    def __repr__(self) -> str:
        return f"<Author {self.ID}: {self.name} from {self.birthplace.city} in {self.birthplace.country}>"
    
    @classmethod
    def from_tuple(cls, t:tuple):
        return Author(t[1], t[2], t[3], t[0])
    
    @classmethod
    def from_id(cls, id:int):
        t = Database.get_by_unique_value(AuthorData.TABLE_NAME, 'id', id)
        if t:
            return Author.from_tuple(t)
    
    @classmethod
    def from_name(cls, name:str):
        t = Database.get_by_unique_value(AuthorData.TABLE_NAME, 'name', name)
        if t:
            return Author.from_tuple(t)

    @classmethod
    def all(cls):
        t = Database.fetch_all(AuthorData.TABLE_NAME)
        l =[]
        for b in t:
            l.append(Author.from_tuple(b))
        return l

    """Helper method. Converts string formated like 'July 31, 1965' time stamp """
    @classmethod
    def str_to_timestamp(cls, date_str:str):
        month = {	'January':'01',
                    'February':'02',
                    'March':'03',
                    'April':'04',
                    'May':'05',
                    'June':'06',
                    'July':'07',
                    'August':'08',
                    'September':'09',
                    'October':'10',
                    'November':'11',
                    'December':'12'	}
        #July 31, 1965 -> '07:31:65'
        date_list = date_str.split(' ')
        date_list[0] = month[date_list[0]]
        date_list[1] = date_list[1][:-1]

        date_str = '-'.join(date_list)

        date = datetime.strptime(date_str, '%m-%d-%Y')

        return datetime.timestamp(date)


    @property
    def birthdate(self):
        return datetime.fromtimestamp(self.birth_timestamp).strftime('%d-%m-%Y')

