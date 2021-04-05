from typing import List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from .. import database, oauth2, schemas
from ..repository import blog

router = APIRouter(tags=['blogs'], prefix='/blog')
get_db = database.get_db


@router.get('', response_model=List[schemas.BlogResponse])
def get_all_posts(db: Session = Depends(get_db),
                  current_user: schemas.User = Depends(
                      oauth2.get_current_user)):
    return blog.get_all(db)


@router.post('', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog,
           db: Session = Depends(get_db),
           user_id: int = 1,
           current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.create(request, db, user_id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id,
                request: schemas.Blog,
                db: Session = Depends(get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.update(id, request, db)


@router.get('/{id}',
            status_code=status.HTTP_200_OK,
            response_model=schemas.BlogResponse)
def get_post(id: int,
             response: Response,
             db: Session = Depends(get_db),
             current_user: schemas.User = Depends(oauth2.get_current_user)):
    return blog.get_one(id, response, db)
