from typing import Any

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Text,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
import dto
from session import AsyncSessionLocal

Base = declarative_base()  # type: Any


async def get_db() -> AsyncSessionLocal:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


def result_to_user(result: User) -> dto.User:
    return dto.User(
        id=dto.UserID(result.id),
        email=result.email,
        created_at=result.created_at,
        updated_at=result.updated_at,
    )