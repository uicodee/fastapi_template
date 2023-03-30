from sqlalchemy import (
    Column,
    DateTime,
    func,
    BigInteger,
)
from sqlalchemy.orm import (
    declarative_base,
)

Base = declarative_base()
metadata = Base.metadata


class BaseModel(Base):
    __abstract__ = True

    id = Column(
        BigInteger,
        nullable=False,
        autoincrement=True,
        primary_key=True,
    )
    created_at = Column(
        DateTime(True),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(True),
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
    )

    def __str__(self):
        return f"{self.id=}\n" \
               f"{self.created_at=}\n" \
               f"{self.updated_at=}"
