from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from typing import Any


class Base(DeclarativeBase):
    id: Any
    __name__: str

    __allow_unmapped__ = True


class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    pomodoro_count = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("Category.id"), nullable=False)

    category = relationship("Category")


class Category(Base):
    __tablename__ = 'Category'
    id: Mapped[int] = Column(Integer, primary_key=True)
    type: Mapped[str] = Column(String, nullable=True)
    name: Mapped[str] = Column(String, nullable=False)
