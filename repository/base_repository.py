from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable, Coroutine, Any, TypeVar

T = TypeVar('T')


class BaseRepository:
    def __init__(self, factory: async_sessionmaker):
        self.factory = factory

    @property
    def session(self):
        return self.factory()

    async def _session_execute(
            self,
            query: Callable[[AsyncSession, ...], Coroutine[Any, Any, T]],
            commit_able: bool = False,
            session: AsyncSession = None,
            *args,
            **kwargs
    ) -> T:
        single_session = False
        if session is None:
            single_session = True
            session = self.session()

        result = await query(session, *args, **kwargs)

        if single_session:
            if commit_able:
                await session.commit()
            await session.close()
        return result
