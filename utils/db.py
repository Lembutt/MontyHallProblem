import sqlite3
import os
import pathlib
from .config import Config
from loguru import logger
conf = Config()


class Database:
    def __init__(self):
        try:
            name = os.path.join(
                    pathlib.Path(__file__).parent,
                    '..',
                    conf.db.name
                )
            print(name)
            self.conn = sqlite3.connect(name)

            self.cur = self.conn.cursor()
        except sqlite3.Error as e:
            logger.error(f"Error occurred while connecting to database. Exception: {e}")

    def close(self):
        if self.conn:
            self.conn.commit()
            self.cur.close()
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self,
                 exc_type,
                 exc_value,
                 traceback):
        self.close()

    def select(self,
               query: str) -> (bool, list):
        if 'select' in query.lower():
            self.cur.execute(query)
            res = self.cur.fetchall()
            return True, res
        raise Exception(
            f"Error occurred in select method of {self.__class__} class. "
            f"There is no 'select' command in query. "
            f"Query: {query}"
        )
   
    def insert(self,
               query: str) -> bool:
        if 'insert' in query.lower():
            self.cur.execute(query)
            return True
        raise Exception(
            f"Error occurred in insert method of {self.__class__} class. "
            f"There is no 'insert' command in query. "
            f"Query: {query}"
        )

    def delete(self,
               query) -> bool:
        if 'delete' in query.lower():
            self.cur.execute(query)
            return True
        raise Exception(
            f"Error occurred in delete method of {self.__class__} class. "
            f"There is no 'delete' command in query. "
            f"Query: {query}"
        )