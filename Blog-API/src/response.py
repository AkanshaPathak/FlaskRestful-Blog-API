from typing import Dict


class Resp:
    def __init__(self):
        self.RESPONSE = {"version": {"version": "1.0.0.0", "name": "web"},
                         "status": {"code": 200, "value": "OK"},
                         "data": None, "error": False}
        self.HEADERS = {"content-type": "application/json",
                        "cache-control": "no-cache"}
        self.USER_CLAIM = None

    def response(self, status_value: Dict) -> Dict:
        self.RESPONSE["status"]["code"] = status_value["code"]
        self.RESPONSE["status"]["value"] = status_value["value"]
        self.RESPONSE["data"] = status_value["data"]
        self.RESPONSE["error"] = status_value.get("error", False)
        return self.RESPONSE

    def http_200(self, **kwargs) -> Dict:
        status = {
            "code": 200,
            "value": "Ok",
            "message": "Success"
        }
        status.update(kwargs)
        return self.response(status)

    def http_201(self, **kwargs) -> Dict:
        status = {
            "code": 201,
            "value": "Created"
        }
        status.update(kwargs)
        return self.response(status)

    def http_203(self, **kwargs) -> Dict:
        status = {
            "code": 203,
            "value": "Non-Authoritative Information"
        }
        status.update(kwargs)
        return self.response(status)

    def http_401(self, **kwargs) -> Dict:
        status = {
            "Code": 401,
            "value": "Unauthorized"
        }
        status.update(kwargs)
        return self.response(kwargs)

    def http_404(self, **kwargs) -> Dict:
        status = {
            "code": 404,
            "value": "Not Found"
        }
        status.update(kwargs)
        return self.response(status)

    def http_405(self, **kwargs) -> Dict:
        status = {
            "code": 405,
            "value": "Not Allowed",
            "data": "Method Not Allowed"
        }
        status.update(kwargs)
        return self.response(status)

    def http_406(self, **kwargs) -> Dict:
        status = {
            "code": 406,
            "value": "Not Acceptable"
        }
        status.update(kwargs)
        return self.response(status)

    def http_409(self, **kwargs) -> Dict:
        status = {
            "code": 409,
            "value": "Conflict"
        }
        status.update(kwargs)
        return self.response(status)

    def http_500(self, **kwargs) -> Dict:
        status = {
            "code": 500,
            "value": "Internal Server Error",
            "data": "Something went wrong"
        }
        status.update(kwargs)
        return self.response(status)
