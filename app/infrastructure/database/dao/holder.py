from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.dao.rdb import BaseDAO


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.base = BaseDAO
