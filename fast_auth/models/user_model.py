from typing import Optional

from sqlalchemy import exc, select
from sqlalchemy.orm import Query

import dto
from exceptions import DuplicateUserError
from models.common import User, result_to_user
from session import AsyncSessionLocal


async def create_user(db_session: AsyncSessionLocal, unsaved_user: dto.UnsavedUser) -> dto.User:
    user = User(**unsaved_user.dict())
    db_session.add(user)
    try:
        await db_session.flush()
    except exc.IntegrityError:
        await db_session.rollback()
        raise DuplicateUserError(f"User with email {unsaved_user.email} already exists.")

    new_user = await find_one(db_session, dto.UserFilter(user_id=dto.UserID(user.id)))
    assert new_user

    return result_to_user(new_user)


async def find_one(
    db_session: AsyncSessionLocal, user_filter: dto.UserFilter
) -> Optional[User]:
    query = select(User)
    query = _filter_to_query(query, user_filter)

    result = await db_session.execute(query)

    rows = result.one_or_none()
    if rows is None:
        return None

    return rows[0]


def _filter_to_query(query: Query, user_filter: dto.UserFilter) -> Query:
    if user_filter.user_id:
        query = query.where(User.id == user_filter.user_id)

    if user_filter.email:
        query = query.where(User.email == user_filter.email)

    return query
