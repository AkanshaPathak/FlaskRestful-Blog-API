# Predefined Libraries
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash

# Service classes
from services.util import Home
from services.user.user import UserRegister, Logout, TokenRefresh
from services.user.validate import ValidateOtp, ResendOtp, ResetPassword, GenerateReset, ValidateReset
from services.org.contact import ContactUs

# Supportive imports
from src.response import Resp
from src.query_base.user_query import User
from src.main_logger import set_up_logging
from blacklist import BLACKLIST

app = Flask(__name__)
CORS(app)
api = Api(app)

resp = Resp()
logger = set_up_logging()

app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]  # allow blacklisting for access and refresh tokens
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
app.secret_key = "_ra/xo$web!@secret#key_"  # could do app.config['JWT_SECRET_KEY'] if we prefer

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    """
        Using the user_claims_loader, we can specify a method that will be
        called when creating access tokens, and add these claims to the said
        token. This method is passed the identity of whom the token is being
        created for, and must return data that is json serializable.
    """
    user_info = resp.USER_CLAIM
    resp.USER_CLAIM = None
    return {
        "Admin": user_info[-2],
        "name": user_info[2],
        "user": {
            "id": identity,
            "public_id": user_info[1],
            "is_active": user_info[-1],
            "email": user_info[4],
        }
    }


class Login(Resource):
    @staticmethod
    def post():
        try:
            data = request.get_json()['data']
            email = data['email']
            password = data['password']
            valid_user = User.user_exists(email)['data']
            valid_user = valid_user[0]
            resp.USER_CLAIM = valid_user
            if not valid_user:
                return resp.http_404(data="You don't have user account.")
            if check_password_hash(valid_user[3], password):
                access_token = create_access_token(identity=valid_user[0], fresh=True)
                refresh_token = create_refresh_token(valid_user[0])
                return resp.http_200(data={"username": valid_user[2], "access-token": access_token,
                                           "refresh-token": refresh_token})
            else:
                return resp.http_401(data="password is not valid")
        except Exception as ex:
            logger.exception(ex)
            return resp.http_500()


api.add_resource(Home, '/')
api.add_resource(UserRegister, '/register')
api.add_resource(ValidateOtp, '/validate-otp')
api.add_resource(Login, '/login')  # Testing required
api.add_resource(Logout, '/logout')  # Testing required
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(ContactUs, '/contact-us')
api.add_resource(ResendOtp, '/resend-otp')
api.add_resource(ResetPassword, '/reset-password')  # first step, Request for url on mail
api.add_resource(GenerateReset, '/forgot-password/<string:hash_val>')  # second step open url and we get hash
api.add_resource(ValidateReset, '/change-password')  # validate hash and change password


if __name__ == '__main__':
    app.run()
