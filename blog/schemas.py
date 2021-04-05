from typing import List

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
