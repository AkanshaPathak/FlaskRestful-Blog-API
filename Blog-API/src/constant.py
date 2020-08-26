class Constant:
    def __init__(self):
        self.RESPONSE = {"version": {"version": "1.0.0.0", "name": "Raxoweb"},
                         "status": {"code": 200, "value": "OK"},
                         "data": None, "error": False}
        self.HEADERS = {"content-type": "application/json",
                        "cache-control": "no-cache"}
        self.USER_CLAIM = None

    def response(self, value, error=False):
        self.RESPONSE["status"]["code"] = value["code"]
        self.RESPONSE["status"]["value"] = value["value"]
        self.RESPONSE["data"] = value["message"]
        if error:
            self.RESPONSE["error"] = True
        return self.RESPONSE
