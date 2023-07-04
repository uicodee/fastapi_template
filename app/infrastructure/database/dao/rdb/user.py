from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import dto
from app.infrastructure.database.dao.rdb import BaseDAO
from app.infrastructure.database.models import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def add_user(
            self,
            firstname: str,
            lastname: str,
            email: str,
            password: str
    ) -> dto.User:
        result = await self.session.execute(
            insert(User).values(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=password
            ).returning(
                User
            )
        )
        await self.session.commit()
        return dto.User.from_orm(result.scalar())

    async def get_user(
            self,
            email: str,
            with_password: bool = False
    ) -> dto.User | dto.UserWithPassword:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar()
        if user is not None:
            if with_password:
                return dto.UserWithPassword.from_orm(user)
            else:
                return dto.User.from_orm(user)
