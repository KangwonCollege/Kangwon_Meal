from sqlalchemy import Result
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.sql import exists

from models import database
from service.base_session import BaseSession


class UserSession(BaseSession):
    def __init__(self, factory: async_sessionmaker):
        super().__init__(factory)

    @staticmethod
    def _get_user_id(argument: discord.User | discord.Member | int) -> int:
        if not isinstance(argument, int) and hasattr(argument, 'id'):
            argument = argument.id
        return argument

    @staticmethod
    async def _is_exist_participant_command(session: AsyncSession, author: int) -> bool:
        query = select(exists(database.UserInfo).where(database.UserInfo.id == author))
        data: Result = await session.execute(query)
        result = data.scalar_one_or_none()
        return bool(result)

    async def is_exist_participant(
            self,
            author: discord.User | discord.Member | int,
            session: AsyncSession = None
    ) -> bool:
        author = self._get_user_id(author)
        result = await self._session_execute(self._is_exist_participant_command, False, session, author=author)
        return bool(result)

    @staticmethod
    async def _get_participant_command(session: AsyncSession, author: int):
        query = select(database.UserInfo).where(database.UserInfo.id == author)
        data: Result = await session.execute(query)
        result = data.scalar_one_or_none()
        return result

    async def get_participant(
            self,
            author: discord.User | discord.Member | int,
            session: AsyncSession = None
    ) -> database.UserInfo:
        author = self._get_user_id(author)
        result = await self._session_execute(self._get_participant_command, False, session, author=author)
        return result
