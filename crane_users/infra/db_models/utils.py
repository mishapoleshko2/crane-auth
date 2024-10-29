from typing import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio.session import AsyncSession

from crane_users.infra.db_models.base import async_session


@asynccontextmanager
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
