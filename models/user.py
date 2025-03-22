from database import Base
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import Column, Integer, String, ForeignKey


class UserProfile(Base):
    __tablename__ = 'UserProfile'
    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String, nullable=False)
    password: Mapped[str] = Column(String, nullable=False)
    access_token: Mapped[str] = Column(String, nullable=False)
