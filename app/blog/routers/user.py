from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from blog import database, schemas
from blog.repository import user

router = APIRouter(tags=['users'], prefix='/user')
get_db = database.get_db


@router.post('', response_model=schemas.UserResponse)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id, db: Session = Depends(get_db)):
    return user.get_one(id, db)
