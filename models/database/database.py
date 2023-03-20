import os, sys


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
        if values:
            cur.execute(query, values)
        else:
            cur.execute(query)
        result = cur.fetchall()
        conn.commit()
        cur.close()
        return result

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

    """Creates new table if not exists."""
    @classmethod
    def create_table_books(cls):
        QUERY = """CREATE TABLE IF NOT EXISTS books(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL UNIQUE,
                        price_cents INTEGER NOT NULL,
                        description TEXT NOT NULL,
                        category TEXT NOT NULL
        );
        """
        Database.execute(QUERY)

    """Printing table in terminal"""
    @classmethod
    def print_table(cls, table_name: str) -> None:
        for x in Database.fetch_all('books'):
            print(x)