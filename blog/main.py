from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import hashing, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blog'])
def create(request: schemas.Blog,
           db: Session = Depends(get_db),
           user_id: int = 1):
    new_post = models.Blog(title=request.title,
                           body=request.body,
                           user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get('/blog', response_model=List[schemas.BlogResponse], tags=['blog'])
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Blog).all()
    return posts


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['blog'])
def delete_post(id, db: Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the id {id} is not found.')
    post.delete(synchronize_session=False)
    db.commit()
    return 'Deleted'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=['blog'])
def update_post(request: schemas.Blog, db: Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the id {id} is not found.')
    post.update(request)
    db.commit()
    return post


@app.get('/blog/{id}',
         status_code=status.HTTP_200_OK,
         response_model=schemas.BlogResponse,
         tags=['blog'])
def get_post(id, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the id {id} is not found.')
    return post


@app.post('/user', response_model=schemas.UserResponse, tags=['user'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):

    new_user = models.User(name=request.name,
                           email=request.email,
                           password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user/{id}', response_model=schemas.UserResponse, tags=['user'])
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with the id {id} is not found.')
    return user
