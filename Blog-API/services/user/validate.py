from flask import request
from flask_restful import Resource
from src.query_base.user_query import ValidateCode, User, ResetHash
import datetime
from library.gmail.mail import mail_otp
from library.otp.otp import generate_otp
from flask import render_template, make_response, redirect
from werkzeug.security import generate_password_hash
from src.response_status import status
from src.main_logger import set_up_logging
from src.constant import Constant
import hashlib

logger = set_up_logging()
constants = Constant()


class ValidateOtp(Resource):
    @staticmethod
    def post():
        data = request.get_json()["data"]
        email = data['email']
        valid_code = ValidateCode.validate_email(email)['data']
        logger.info(f"Validate code: {valid_code}")
        try:
            # Code Found but Expired
            if datetime.datetime.now() > valid_code[0][1]:
                ValidateCode.delete_code(email)
                status[406]["message"] = "OTP is expired"
                return constants.response(status[406])
            if int(data['code']) == valid_code[0][0]:
                ValidateCode.delete_code(email)
                User.activate_user(email)
                status[201]["message"] = "User account activated"
                return constants.response(status[201])

            if int(data['code']) != valid_code[0][0]:
                status[203]["message"] = "OTP is not valid"
                return constants.response(status[203])
        except Exception as ex:
            logger.exception(ex)
            return constants.response(status[500])


class ResendOtp(Resource):

    @staticmethod
    def post():
        try:
            email = request.get_json()["data"]["email"]
            otp, expire_time = generate_otp()
            mail_otp(email, str(otp), "User")
            ValidateCode.insert_code(email, otp, expire_time)
            status[201]["message"] = "OTP is sent to register email"
            return constants.response(status[201])
        except Exception as ex:
            logger.exception(ex)
            return constants.response(status[500])


class ResetPassword(Resource):
    @staticmethod
    def post():
        try:
            email = request.get_json()['data']['email']
            user = User.user_exists(email)["data"]
            if user and user[0][0]:
                code = hashlib.md5(str.encode(email)).hexdigest()
                salt1 = "c2h56a7n3d25a1n9"
                salt2 = "c94h6a78i42n91a73n58i"
                final_code = salt1 + code + salt2
                ResetHash.insert_hash(email, final_code)
                url = "http://127.0.0.1:5000/forgot-password/" + final_code
                mail_otp(email, url, user[0][1])
                status[200]["message"] = "Mail sent to the user"
                return constants.response(status[200])
            else:
                status[404]["message"] = "User not found"
                return constants.response(status[404])
        except Exception as ex:
            logger.exception(ex)
            return constants.response(status[500])


class GenerateReset(Resource):
    def __init__(self):
        pass

    @staticmethod
    def get(hash_val):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', email=hash_val), 200, headers)


class ValidateReset(Resource):
    @staticmethod
    def post():
        data = request.get_json()["data"]
        password = data['password']
        hash_val = data['hash']
        try:
            hash_info = ResetHash.hash_exists(hash_val)['data']
            if hash_info:
                email = hash_info[0][0]
                hash_password = generate_password_hash(password, method='sha256')
                User.change_password(hash_password, email)
                ResetHash.delete_hash(hash_val)
                return redirect("https://www.raxoweb.com", code=302)
            else:
                status[203]['message'] = "your information is not correct"
                return constants.response(status[203])
        except Exception as ex:
            logger.exception(ex)
            return constants.response(status[500])
