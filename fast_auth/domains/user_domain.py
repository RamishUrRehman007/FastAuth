from typing import Optional

from passlib.context import CryptContext

import dto
from session import AsyncSessionLocal
from models import user_model
from models.common import User, result_to_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register_user(db_session: AsyncSessionLocal, unsaved_user: dto.UnsavedUser) -> dto.User:
    unsaved_user.password = pwd_context.hash(unsaved_user.password)
    new_user = await user_model.create_user(db_session, unsaved_user)
    await db_session.commit()

    return new_user


async def auth_user(
    db_session: AsyncSessionLocal,
    auth_user: dto.AuthUser
) -> Optional[dto.User]:
    
    unverified_user = await user_model.find_one(db_session, dto.UserFilter(email=auth_user.email))
    if not unverified_user:
        return None
    
    verified_user = _verify_password(unverified_user, auth_user.password)

    return verified_user


async def get_user(
    db_session: AsyncSessionLocal,
    user_filter: dto.UserFilter
) -> Optional[dto.User]:
    result =  await user_model.find_one(db_session, user_filter)
    return result_to_user(result) if result else None


def _verify_password(result: User, password: str) -> Optional[dto.User]:
    return result_to_user(result) if pwd_context.verify(password, result.password) else None