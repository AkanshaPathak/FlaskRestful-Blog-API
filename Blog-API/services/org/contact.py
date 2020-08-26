from flask_restful import Resource
from library.gmail.mail import mail_info, mail_me
from flask import request
from src.constant import Constant
from src.response_status import status
from src.main_logger import set_up_logging
from src.query_base.org_query import Contact
constants = Constant()
logger = set_up_logging()


class ContactUs(Resource):
    @staticmethod
    def post():
        try:
            data = request.get_json()['data']
            firstname = data.get('firstname', 'User')
            lastname = data.get('lastname')
            email = data.get('email')
            mobile_no = data.get('mobile')
            message = data.get('message')
            mail_info(email, firstname)
            mail_me(firstname, email, mobile_no, message)
            Contact.insert_info(firstname, lastname, email, mobile_no, message)
            status[200]['message'] = "we will contact you soon"
            return constants.response(status[200])
        except Exception as ex:
            logger.info(ex)
            return constants.response(status[500])
