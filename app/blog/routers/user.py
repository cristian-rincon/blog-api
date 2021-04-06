import csv
from io import StringIO

from fastapi import APIRouter, Depends, File
from sqlalchemy.orm import Session

from blog import database, oauth2, schemas
from blog.repository import user

router = APIRouter(tags=['users'], prefix='/user')
get_db = database.get_db


@router.post('', response_model=schemas.UserResponse)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id, db: Session = Depends(get_db)):
    return user.get_one(id, db)


@router.post('/bulk')
def bulk_load_users(file: bytes = File(...),
                    db: Session = Depends(get_db),
                    current_user: schemas.User = Depends(
                        oauth2.get_current_user)):

    content = file.decode()
    file = StringIO(content)
    reader = csv.reader(file, delimiter=",")
    header = next(reader)
    data = []
    if header is not None:
        for row in reader:
            data.append(tuple(row))

    user.bulk_load(data, db)
    return f'{len(data)} users loaded'
