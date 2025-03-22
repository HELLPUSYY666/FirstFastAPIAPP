from sqlalchemy.orm import DeclarativeBase
from typing import Any


class Base(DeclarativeBase):
    id: Any
    __name__: str

    __allow_unmapped__ = True

