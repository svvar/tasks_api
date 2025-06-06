from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from database import User


async def insert_user(
        session: AsyncSession,
        email: str,
        password_hash: str,
        first_name: str = None,
        last_name: str = None
) -> User:
    async with session:
        new_user = User(
            email=email,
            password=password_hash,
            first_name=first_name,
            last_name=last_name
        )
        session.add(new_user)
        try:
            await session.commit()
            return new_user
        except IntegrityError:              # won't check for asyncpg UniqueViolationError, any other IntegrityError shouldn't happen here
            await session.rollback()
            raise ValueError("User with this email already exists")


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    async with session:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()