from flask import request
from flask_restful import Resource
from src.query_base.user_query import User, ValidateCode
from library.gmail.mail import mail_otp
from werkzeug.security import generate_password_hash
from library.otp.otp import generate_otp
from src.constant import Constant
from src.main_logger import set_up_logging
from src.response_status import status
from blacklist import BLACKLIST
import uuid
from flask_jwt_extended import (
    create_access_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)

constants = Constant()
logger = set_up_logging()


# username, userpic, title , photo, content , category , time , hona chahiye

class UserRegister(Resource):
    @staticmethod
    def post():
        data = request.get_json()['data']
        past_user = User.user_exists(data['email'])["data"]
        logger.info(past_user)
        if past_user and past_user[0][0] and past_user[0][1]:
            status[409]["message"] = "A user with this email already exists"
            return constants.response(status[409])
        try:
            hash_password = generate_password_hash(data['password'], method='sha256')
            out = User.create_user(data['username'], hash_password, data['email'], str(uuid.uuid4()))
            logger.info(out)
            otp, expire_time = generate_otp()
            """send mail to user for otp"""
            mail_otp(data['email'], str(otp), data['username'])
            logger.info(f"OTP: {otp}, Expire Time: {expire_time}")
            ValidateCode.insert_code(data['email'], otp, expire_time)
            status[201]["message"] = "User created successfully."
            return constants.response(status[201])
        except Exception as ex:
            logger.exception(ex)
            return constants.response(status[500])


class Logout(Resource):
    @jwt_required
    def token_check(self):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return user_id

    def post(self):
        try:
            user_id = self.token_check()
            status[200]['message'] = "User id: {} successfully logged out.".format(user_id)
            return constants.response(status[200])
        except Exception as ex:
            logger.exception(ex)
            return constants.response(status[500])


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        status[200]['message'] = new_token
        return constants.response(status[200])
