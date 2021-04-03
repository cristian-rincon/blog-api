# 2.51 - https://www.youtube.com/watch?v=7t2alSnE2-I
# import uvicorn
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.get('/blog')
# Query params sample
def index(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        response = {"data": [limit]}
    else:
        response = None
    return response


@app.get('/blog/unpublished')
def get_unpublished_post():
    return {'data': {}}


@app.get('/blog/{id}')
def get_post(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def get_post_comments(id: int, limit: int = 10):
    return {'data': {'comments': {'1', '2'}}}


@app.get('/about')
def about():
    return {
        'data': {
            "about": "page"
        }
    }


@app.post('/blog')
def create_post(blog: Blog):
    return {'data': blog}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=9000)
