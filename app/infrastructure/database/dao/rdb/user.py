from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.api import schems
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def add_user(self, user: schems.User) -> dto.User:
        user = User(**user.dict())
        self.session.add(user)
        await self.session.commit()
        return dto.User.from_orm(user)

    async def get_user(
        self, email: str, with_password: bool = False
    ) -> dto.User | dto.UserWithPassword:
        result = await self.session.execute(select(User).where(User.email == email))
        user = result.scalar()
        if user is not None:
            if with_password:
                return dto.UserWithPassword.from_orm(user)
            else:
                return dto.User.from_orm(user)
