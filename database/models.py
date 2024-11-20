from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pass

class Task(Base):
    __tablename__ = "Tasks"
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(60))
    owner: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Task(id={self.id}, name={self.name}, description={self.description})"

class User(Base):
    __tablename__ = "Users"
    login: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(30))

    def __repr__(self) -> str:
        return f"Task(id={self.id}, login={self.login}, password={self.password})"

class Token_validation(Base):
    __tablename__ = "Token_validation"
    user_id: Mapped[str] = mapped_column(String(30), ForeignKey("Users.id"))
    jwt: Mapped[str] = mapped_column(String(100))



