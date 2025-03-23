from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import insert, select
from models import UserProfile


@dataclass
class UserRepository:
    session_maker: async_sessionmaker[AsyncSession]

    async def create_user(self, username: str, password: str) -> UserProfile:
        query = insert(UserProfile).values(
            username=username,
            password=password,
        ).returning(UserProfile.id)

        async with self.session_maker() as session:
            result = await session.execute(query)
            user_id = result.scalar_one()
            await session.commit()
            return await self.get_user(user_id, session=session)

    async def get_user(self, user_id: int, session: AsyncSession | None = None) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)

        if session is None:
            async with self.session_maker() as session:
                result = await session.execute(query)
                return result.scalar_one_or_none()
        else:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.session_maker() as session:
            result = await session.execute(query)
            return result.scalars().first()
