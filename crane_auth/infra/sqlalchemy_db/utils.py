from typing import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio.session import AsyncSession

from crane_auth.infra.sqlalchemy_db.base import async_session


async def get_session(with_commit: bool = False) -> AsyncIterator[AsyncSession]:
    try:
        async with async_session() as session:
            yield session
        if with_commit:
            await session.commit()
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


get_context_session = asynccontextmanager(get_session)
