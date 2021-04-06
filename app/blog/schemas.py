from typing import List, Optional

from pydantic import BaseModel


class BaseBlog(BaseModel):
    title: str
    body: str


class Blog(BaseBlog):

    class Config():
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []

    class Config():
        orm_mode = True


class BlogResponse(Blog):
    title: str
    body: str
    creator: UserResponse

    class Config():
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
