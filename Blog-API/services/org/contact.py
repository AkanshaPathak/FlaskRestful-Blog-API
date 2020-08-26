from flask_restful import Resource
from library.gmail.mail import mail_info, mail_me
from flask import request
from src.response import Resp
from src.main_logger import set_up_logging
from src.query_base.org_query import Contact

resp = Resp()
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
            return resp.http_200(data="we will contact you soon")
        except Exception as ex:
            logger.info(ex)
            return resp.http_500()
