from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base_model(DeclarativeBase):
    __tablename__ = "tasks"
    id : Mapped[int] = mapped_column(primary_key=True)

class Task(Base_model):
    name: Mapped[str]
    description: Mapped[str]