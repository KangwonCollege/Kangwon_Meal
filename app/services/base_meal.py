import aiohttp

from ahttp_client import Session
from app.services.errors import HttpException, NotFound, InternalServerError


class BaseMeal(Session):
    def __init__(self, base_url: str, **kwargs):
        super().__init__(
            base_url=base_url,
            connector=aiohttp.TCPConnector(ssl=False)
        )

    async def after_request(self, response: aiohttp.ClientResponse):
        if response.status == 404:
            text = await response.text()
            raise NotFound(response.status, text)
        elif response.status >= 500:
            raise InternalServerError(response.status)
        elif response.status > 400:
            raise HttpException(response.status)
        return response
