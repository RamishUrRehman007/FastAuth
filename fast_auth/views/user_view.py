from typing import Any

import dto
from domains import user_domain
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi_csrf_protect import CsrfProtect
from fastapi_jwt_auth import AuthJWT
from models.common import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/auth/register",
    response_model=dto.User,
    status_code=status.HTTP_201_CREATED,
    tags=["auth"],
)
async def register_user(
    unsaved_user: dto.UnsavedUser,
    db_session: Session = Depends(get_db),
) -> dto.User:
    """
    Create view for creating a new User given an UnsavedUser payload.

    \f
    :return:
    """

    return await user_domain.register_user(db_session, unsaved_user)


@router.post(
    "/auth/login",
    response_model=Any,
    status_code=status.HTTP_200_OK,
    tags=["auth"],
)
async def login(
    auth_user: dto.AuthUser,
    db_session: Session = Depends(get_db),
    authorize: AuthJWT = Depends(),
    csrf_protect: CsrfProtect = Depends(),
) -> Any:
    """
    Auth view for generating auth tokens given an AuthUser payload.

    \f
    :return:
    """

    user = await user_domain.auth_user(db_session, auth_user)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    content = {"message": "Login Successfully"}
    response = JSONResponse(content=content)

    response.set_cookie(
        key="access_token", value=authorize.create_access_token(subject=user.email)
    )
    response.set_cookie(
        key="refresh_token", value=authorize.create_refresh_token(subject=user.email)
    )
    csrf_protect.set_csrf_cookie(response)

    return response


@router.get(
    "/auth/user",
    response_model=dto.User,
    tags=["auth"],
)
async def get_user(
    request: Request,
    db_session: Session = Depends(get_db),
) -> dto.User:
    """
    To get User.
    \f
    :return:
    """
    user = await user_domain.get_user(
        db_session, dto.UserFilter(email=request.state.user_email)
    )
    assert user

    return user
