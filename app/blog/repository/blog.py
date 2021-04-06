from fastapi import HTTPException, Response, status
from sqlalchemy.orm import Session

from blog import models, schemas


def get_all(db: Session):
    posts = db.query(models.Blog).all()
    return posts


def create(request: schemas.Blog, db: Session, user_id):
    new_post = models.Blog(title=request.title,
                           body=request.body,
                           user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def delete(id: int, db: Session):
    post = db.query(models.Blog).filter(models.Blog.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the id {id} is not found.')
    post.delete(synchronize_session=False)
    db.commit()


def update(id: int, request: schemas.Blog, db: Session):
    post = db.query(models.Blog).filter(models.Blog.id == id)
    found_blog = post.first()
    if found_blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    post.update(dict(request))
    db.commit()
    return 'updated'


def get_one(id: int, response: Response, db: Session):
    post = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with the id {id} is not found.')
    return post


def bulk_load(data, db: Session):
    for i in data:
        new_post = models.Blog(title=i[0], body=i[1], user_id=i[2])
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    return len(data)
