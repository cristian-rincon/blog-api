from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from blog import models
from blog.database import engine
from blog.routers import authentication, blog, user

models.Base.metadata.create_all(engine)
app = FastAPI(title="Blog API")

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)


@app.get('/')
def index():
    return RedirectResponse('/docs')
