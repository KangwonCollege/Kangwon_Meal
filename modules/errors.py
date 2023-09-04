from typing import Any


class HttpException(Exception):
    def __init__(self, response_code: int, data: dict[str, Any]):
        self.response_code = response_code
        self.data = data
        super(HttpException, self).__init__("HTTP Response Error: {}".format(response_code))


class NotFound(HttpException):
    """유저를 찾지 못할때 발생합니다."""
    pass


class InternalServerError(HttpException):
    """API 서버에서 문제가 발생 했을 때, 발생하는 예외입니다."""
    pass
