from mysql import connector
from src.main_logger import set_up_logging
import json

logger = set_up_logging()


class Database:
    def __init__(self):
        self.__get_config()
        self.__create_connection()

    def __enter__(self):
        return self

    def __del__(self, exc_type, exc_val, exc_tb):
        self.__close__()

    def __close__(self):
        self._cursor.close()
        self._connection.close()

    # Below are all private functions to be used within this class

    def __get_config(self):
        with open("src/mysql_db.json", 'r') as file:
            self.config = json.load(file)['mysql']
        logger.info(self.config)
        return self.config

    def __create_connection(self):
        self._connection = connector.connect(**self.config)
        return self._connection

    # cursor is private,
    # you can use this to do database operation inside derived class if Inheriting Database class.
    def __create_cursor(self):
        self._cursor = self._connection.cursor(dictionary=True)
        return self._cursor

    def __execute(self, query):
        try:
            self._cursor.execute(query)
            self._connection.commit()
            return 1
        except Exception as ex:
            logger.exception(ex)
            return 0
        finally:
            self.__close__()

    # Below are public functions to be called for database operation.

    def select(self, query):
        try:
            self._cursor.execute(query)
            query_result = self._cursor.fetchall()
            total_rows = self._cursor.rowcount
            resp = {'data': query_result,
                    "row_count": total_rows,
                    'sqlerror': False
                    }
            return resp
        except Exception as ex:
            return {'data': {},
                    'sqlError': str(ex)
                    }
        finally:
            self.__close__()

    def insert(self, query):
        return self.__execute(query)

    def update(self, query):
        return self.__execute(query)

    def delete(self, query):
        return self.__execute(query)
