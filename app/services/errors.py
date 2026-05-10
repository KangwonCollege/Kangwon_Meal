from typing import Optional


class HttpException(Exception):
    def __init__(self, response_code: int, data: Optional[str] = None):
        self.response_code = response_code
        self.data = data
        super().__init__("HTTP Response Error: {}".format(response_code))


class NotFound(HttpException):
    pass


class InternalServerError(HttpException):
    pass
