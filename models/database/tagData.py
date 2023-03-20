from database import Database

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
    
TagData.insert('love')
Database.print_table(TagData.TABLE_NAME)