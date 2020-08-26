from library.db.db import Database
from src.main_logger import set_up_logging

database = Database()
logger = set_up_logging()


class User:
    @staticmethod
    def user_exists(email):
        query = f"select id, public_id, username, password, email, admin, is_active from users where email = '{email}';"
        return database.receive_query(query)

    @staticmethod
    def create_user(username, password, email, public_id, is_admin=0, is_active=0):
        query = f"INSERT INTO users (public_id, username, password, email, admin, is_active) VALUES('{public_id}'," \
                f" '{username}', '{password}', '{email}', {is_admin}, {is_active}) ON DUPLICATE KEY UPDATE " \
                f"username='{username}', password='{password}', admin={is_admin};"
        return database.insert_query(query)

    @staticmethod
    def activate_user(email):
        query = f"UPDATE users SET is_active=1 WHERE email='{email}';"
        return database.update_query(query)

    @staticmethod
    def change_password(password, email):
        query = f"UPDATE users set password = '{password}' where email = '{email}';"
        database.update_query(query)


class ValidateCode:
    @staticmethod
    def validate_email(email):
        query = f"select code, expiretime from validate_code where email = '{email}'"
        return database.receive_query(query)

    @staticmethod
    def delete_code(email):
        query = f"DELETE FROM validate_code WHERE email='{email}';"
        return database.delete(query)

    @staticmethod
    def insert_code(email, code, expire_time):
        query = f"INSERT INTO validate_code (email, code, expiretime)VALUES('{email}', {code}, '{expire_time}') ON " \
                f"DUPLICATE KEY UPDATE code = {code}, expiretime='{expire_time}'; "
        logger.info(f"Insert OTP query: {query}")
        return database.insert_query(query)


class ResetHash:
    @staticmethod
    def insert_hash(email, hash_code):
        query = f"INSERT INTO ResetHash (email, hash) VALUES('{email}', '{hash_code}') ON DUPLICATE KEY UPDATE" \
                f" email='{email}', hash='{hash_code}';"
        database.insert_query(query)

    @staticmethod
    def hash_exists(hash_value):
        query = f"select email from ResetHash where hash = '{hash_value}'"
        logger.info(query)
        return database.receive_query(query)

    @staticmethod
    def delete_hash(hash_val):
        query = f"DELETE FROM ResetHash WHERE hash='{hash_val}';"
        database.delete(query)
