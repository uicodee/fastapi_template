from app.dto import Base


class User(Base):

    firstname: str
    lastname: str
    email: str


class UserWithPassword(User):

    password: str
