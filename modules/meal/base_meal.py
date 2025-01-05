import asyncio
import aiohttp

from ahttp_client import Session
from .errors import *

class BaseMeal(Session):
    def __init__(self, base_url: str, loop: asyncio.AbstractEventLoop, **kwargs):
        self.loop = loop
        super().__init__(
            base_url=base_url,
            loop=loop,
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