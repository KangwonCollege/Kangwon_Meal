import aiohttp
import asyncio

from typing import Type
from modules.errors import (
    HttpException,
    NotFound,
    InternalServerError,
)
from modules.response import Response


class Requests:
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        session: aiohttp.ClientSession = None,
        e404: Type[NotFound] = None,
        e500: Type[InternalServerError] = None,
        **kwargs
    ):
        self.loop = loop or asyncio.get_event_loop()
        self.session = session

        self.e404 = e404 or NotFound
        self.e500 = e500 or InternalServerError
        self.session_option = kwargs

    @staticmethod
    async def divide_content(resp):
        if resp.content_type.startswith("application/json"):
            return await resp.json()
        elif resp.content_type.startswith("image/"):
            return await resp.content.read()
        elif resp.content_type.startswith("text/html"):
            return await resp.text()
        else:
            return None

    async def requests(
            self,
            method: str,
            url: str,
            raise_on: bool = False,
            **kwargs
    ) -> Response:
        single_session = False
        session = self.session

        if session is None:
            single_session = True
            session = aiohttp.ClientSession(
                loop=self.loop,
                connector=aiohttp.TCPConnector(ssl=False),
                **self.session_option
            )

        async with session.request(method, url, **kwargs) as response:
            data = await self.divide_content(response)
            request_data = Response(
                status=response.status,
                data=data,
                version=response.version,
                content_type=response.content_type,
                reason=response.reason,
                headers=response.headers,
            )

            if raise_on:
                if request_data.status == 404:
                    raise self.e404(response.status, data)
                elif request_data.status == 500:
                    raise self.e500(response.status, data)
                elif request_data.status >= 300:
                    raise HttpException(response.status, data)

        if single_session:
            await session.close()
        return request_data

    async def get(self, url: str, raise_on: bool = False, **kwargs):
        return await self.requests(method="GET", url=url, raise_on=raise_on, **kwargs)

    async def post(self, url: str, raise_on: bool = False, **kwargs):
        return await self.requests(method="POST", url=url, raise_on=raise_on, **kwargs)