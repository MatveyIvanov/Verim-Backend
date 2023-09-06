from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependency_injector.wiring import Provide, inject

from config.di import Container
from models.users import User


router = APIRouter()


def get_db():
    from config.db import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
@inject
async def test(db: Session = Depends(get_db)):
    print(db.query(User).all())
    return {'message': 'Testing application'}
