
import sqlite3


class Database:
    DATABASE_FILE ='data.sqlite'


    """Execute a query on database."""
    @classmethod
    def execute(cls, query: str, values:tuple = None, file_name: str =DATABASE_FILE) -> None:
        conn = sqlite3.connect(file_name)
        cur = conn.cursor()
        cur.execute('PRAGMA foreign_key=on;')
        if values:
            cur.execute(query, values)
        else:
            cur.execute(query)
        
        conn.commit()
        conn.close()

    """General fetch method helping with getting entries from database."""
    @classmethod
    def fetch_all(cls, table_name, limit:int = None, offset:int=None, file_name:str = DATABASE_FILE) -> list[tuple]:
        conn = sqlite3.connect(file_name)
        cur = conn.cursor()
        cur.execute('PRAGMA foreign_key=on;')
        if limit and offset:
            cur.execute(f"SELECT * FROM {table_name} LIMIT {limit} OFFSET {offset};")
        elif limit:
            cur.execute(f"SELECT * FROM {table_name} LIMIT {limit};")
        elif offset:
            cur.execute(f"SELECT * FROM {table_name} OFFSET {offset};")
        else:
            cur.execute(f"SELECT * FROM {table_name};")
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result

    """Fetch directly from query."""
    @classmethod
    def query_fetch(cls, query:str, values:tuple =None, file_name:str = DATABASE_FILE) -> list[tuple]:
        conn = sqlite3.connect(file_name)
        cur = conn.cursor()
        cur.execute('PRAGMA foreign_key=on;')
        if values:
            cur.execute(query, values)
        else:
            cur.execute(query)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result

    """Insert values into table. Don't allow users to type value_names."""
    @classmethod
    def unsafe_insert(cls, table_name:str, value_names:tuple[str], values:tuple):
        value_names_str = ''
        question_marks_str = ''

        for name in value_names:
            value_names_str += name + ", "
            question_marks_str += "?, "

        #removes trailing comas and spaces
        value_names_str = value_names_str[:-2]
        question_marks_str = question_marks_str[:-2]

        QUERY = f'INSERT INTO {table_name} ({value_names_str}) VALUES ({question_marks_str});'
        Database.execute(QUERY, values)

    """Get record by value or empty tuple if record does not exist. If many record with the same value returns first."""
    @classmethod
    def get_by_unique_value(cls, table_name:str, value_name:str, value) -> tuple:
        r = Database.query_fetch(f"SELECT * FROM {table_name} WHERE {value_name} = ?;", (value,))
        if r:
            return r[0]
        else:
            tuple()

    """Check if unique value is taken by existing entry."""
    @classmethod
    def is_unique_value_free(cls, table_name:str, value_name:str, value) -> bool:
        return not Database.get_by_unique_value(table_name, value_name, value)

    """Creates new tables if not exists."""
    @classmethod
    def create_tables(cls):
        LOCATIONS_TABLE = """   CREATE TABLE IF NOT EXISTS locations (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    city TEXT NOT NULL,
                                    country TEXT NOT NULL
                                );
        """

        AUTHORS_TABLE = """     CREATE TABLE IF NOT EXISTS authors(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT NOT NULL UNIQUE,
                                    birthplace INTEGER NOT NULL,
                                    birthdate INTEGER NOT NULL,
                                    FOREIGN KEY (birthplace) REFERENCES locations(id)
                                );
        """

        TAGS_TABLE = """        CREATE TABLE IF NOT EXISTS tags(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name TEXT UNIQUE NOT NULL
                                );
        """

        QUOTES_TABLE = """      CREATE TABLE IF NOT EXISTS quotes(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    author_id INTEGER NOT NULL,
                                    quote TEXT NOT NULL UNIQUE,
                                    FOREIGN KEY (author_id) REFERENCES authors(id)
                                );   
        """

        QUOTES_TAGS_TABLE = """ CREATE TABLE IF NOT EXISTS quotes_tags(
                                    tag_id INTEGER NOT NULL,
                                    quote_id INTEGER NOT NULL,
                                    FOREIGN KEY (tag_id) REFERENCES tags(id),
                                    FOREIGN KEY (quote_id) REFERENCES quotes(id)
                                );
        """        

        Database.execute(LOCATIONS_TABLE)
        Database.execute(AUTHORS_TABLE)
        Database.execute(TAGS_TABLE)
        Database.execute(QUOTES_TABLE)
        Database.execute(QUOTES_TAGS_TABLE)

    """Printing table in terminal"""
    @classmethod
    def print_table(cls, table_name: str) -> None:
        for x in Database.fetch_all(table_name):
            print(x)

Database.create_tables()