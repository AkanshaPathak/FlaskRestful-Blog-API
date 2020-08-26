from mysql import connector
from mysql.connector import FieldType
from src.main_logger import set_up_logging
import json

logger = set_up_logging()


class Database:
    def __init__(self, config=None):
        self.config = self.get_config(config)

    @staticmethod
    def get_config(config):
        db_name = "mysql" if not config else config
        with open("src/mysql_db.json", 'r') as file:
            db_config = json.load(file)[db_name]
        logger.info(db_config)
        return db_config

    def connection(self, query, cursor_type, metadata=False):
        connection = connector.connect(**self.config)
        cursor = connection.cursor(cursor_type)
        cursor.execute(query)
        query_result = cursor.fetchall()
        if metadata:
            total_rows = cursor.rowcount
            meta_data = []
            for col_index, desc in enumerate(cursor.description):
                meta_data.append({'colIndex': col_index,
                                  'colName': desc[0],
                                  'colType': FieldType.get_info(desc[1])})
            out = (meta_data, total_rows, query_result)
        else:
            out = query_result
        cursor.close()
        connection.close()
        return out

    def set_data(self, query):
        try:
            connection = connector.connect(**self.config)
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return {'data': 1,
                    'error': False,
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}

        except Exception as ex:
            return {'data': 0,
                    'sqlError': str(ex),
                    'error': False,
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}

    def execute_query(self, query, cursor_type='list'):
        try:
            query_result = self.connection(query, cursor_type)
            resp = {'data': {'result': {'metaData': query_result[0],
                                        'queryInfo': {'totalRows': query_result[1], 'type': 'selected'},
                                        'resultSet': query_result[2]}},
                    'error': False,
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}
            return resp
        except Exception as ex:
            return {'data': None,
                    'error': False,
                    'sqlError': str(ex),
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}

    def receive_query(self, query, cursor_type='dict'):
        try:
            query_result = self.connection(query, cursor_type)
            resp = {'data': query_result,
                    'error': False,
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}
            return resp

        except Exception as ex:

            return {'data': None,
                    'error': False,
                    'sqlError': str(ex),
                    'status': {'code': '200', 'value': 'Success'},
                    'version': {'name': 'Raxoweb', 'version': '1.0.0.0'}}

    def insert_query(self, query):
        return self.set_data(query)

    def update_query(self, query):
        return self.set_data(query)

    def delete(self, query):
        return self.set_data(query)
