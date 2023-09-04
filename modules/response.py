

class Response:
    def __init__(self, status: int, **kwargs):
        self.status = status
        self.data = kwargs["data"]
        self.headers: dict[str, str] = kwargs["headers"]

        self.version: str = kwargs.get("version")
        self.content_type = kwargs.get("content_type") or self.headers.get("Content-Type")
        self.reason = kwargs.get("reason")
