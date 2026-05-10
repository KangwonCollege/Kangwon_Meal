from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_session(request: Request) -> AsyncSession:
    session = request.app.state.session_factory()
    try:
        yield session
    finally:
        await session.close()
