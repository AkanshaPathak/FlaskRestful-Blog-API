from flask_restful import Resource
from src.response import Resp

resp = Resp()


class Home(Resource):
    @staticmethod
    def get():
        return resp.http_405()

    @staticmethod
    def post():
        return resp.http_200()
