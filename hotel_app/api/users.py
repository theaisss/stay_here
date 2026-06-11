from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import UserProfile, RoleChoices
from hotel_app.database.schema import UserProfileInputSchema, UserProfileOutSchema
from hotel_app.database.db import SessionLocal

user_router = APIRouter(prefix='/users', tags=['Users CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post('/', response_model=UserProfileOutSchema)
async def user_create(user: UserProfileInputSchema, db: Session = Depends(get_db)):
    data = user.model_dump()
    if 'user_role' in data:
        data['user_role'] = RoleChoices(data['user_role'])
    user_db = UserProfile(**data)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.get('/', response_model=List[UserProfileOutSchema])
async def user_list(db: Session = Depends(get_db)):
    return db.query(UserProfile).all()

@user_router.get('/{user_id}', response_model=UserProfileOutSchema)
async def user_detail(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='That not information', status_code=404)
    return user_db

@user_router.put('/{user_id}', response_model=dict)
async def update_user(user_id: int, user: UserProfileInputSchema, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='That not information', status_code=404)
    for user_key, user_value in user.model_dump().items():
        if user_key == 'user_role' and user_value is not None:
            user_value = RoleChoices(user_value)
        setattr(user_db, user_key, user_value)
    db.commit()
    return {'message': 'Users updated'}

@user_router.delete('/{user_id}', response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(detail='That not information', status_code=404)
    db.delete(user_db)
    db.commit()
    return {'message': 'Users deleted'}