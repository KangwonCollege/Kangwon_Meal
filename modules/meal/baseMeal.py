import asyncio

from modules.requests import Requests


class BaseMeal:
    def __init__(self, loop: asyncio.AbstractEventLoop, **kwargs):
        self.loop = loop
        self.requests = Requests(self.loop, **kwargs)
