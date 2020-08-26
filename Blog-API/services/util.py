from flask_restful import Resource
from src.constant import Constant
from src.response_status import status

constants = Constant()


class Home(Resource):
    @staticmethod
    def get():
        return constants.response(status[405])

    @staticmethod
    def post():
        return constants.response(status[200])
