from sqlalchemy.orm import sessionmaker

from app.infrastructure.database.dao import HolderDao


def dao_provider():
    ...


class DbProvider:
    def __init__(self, pool: sessionmaker):
        self.pool = pool

    async def dao(self):
        async with self.pool() as session:
            yield HolderDao(session=session)
