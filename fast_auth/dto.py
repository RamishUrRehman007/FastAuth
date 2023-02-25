from typing import List, Optional, Dict, Any, NewType
from datetime import datetime
from typing import List, NewType, Optional, TypeVar
from pydantic import BaseModel, ConstrainedStr, EmailStr

UserID = NewType("UserID", int)
ResponseT = TypeVar("ResponseT")
JSON = Dict[str, Any]


class RequiredStr(ConstrainedStr):
    strip_whitespace = True
    min_length = 8


class UnsavedUser(BaseModel):
    email: EmailStr
    password: RequiredStr


class User(BaseModel):
    id: UserID
    email: str
    created_at: datetime
    updated_at: datetime


class UserFilter(BaseModel):
    user_id: Optional[UserID] = None
    email: Optional[str] = None
    password: Optional[str] = None


class AuthUser(BaseModel):
    email: EmailStr
    password: RequiredStr


class ErrorResponse(BaseModel):
    detail: str


class LinkResponse(BaseModel):
    href: str
    rel: str
    type: str


class StatusViewResponse(BaseModel):
    service: str
    version: str
    environment: str
    links: Optional[List[LinkResponse]]
