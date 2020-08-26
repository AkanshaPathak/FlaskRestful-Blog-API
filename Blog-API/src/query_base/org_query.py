from library.db.db import Database

database = Database()


class Contact:
    @staticmethod
    def insert_info(firstname, lastname, email, mobile_no, message):
        query = f"INSERT INTO raxoweb.ContactUs (firstname, lastname, email, mobile_no, message) VALUES('{firstname}'," \
                f" '{lastname}', '{email}', {mobile_no}, '{message}');"
        database.insert_query(query)
