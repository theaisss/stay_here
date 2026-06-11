from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import RoomImage
from hotel_app.database.schema import RoomImageInputSchema, RoomImageOutSchema
from hotel_app.database.db import SessionLocal

room_image_router = APIRouter(prefix='/room-images', tags=['Room Image CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@room_image_router.post('/', response_model=RoomImageOutSchema)
async def room_image_create(image: RoomImageInputSchema, db: Session = Depends(get_db)):
    db_obj = RoomImage(**image.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@room_image_router.get('/', response_model=List[RoomImageOutSchema])
async def room_image_list(db: Session = Depends(get_db)):
    return db.query(RoomImage).all()

@room_image_router.get('/{image_id}', response_model=RoomImageOutSchema)
async def room_image_detail(image_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(RoomImage).filter(RoomImage.id == image_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@room_image_router.put('/{image_id}', response_model=dict)
async def room_image_update(image_id: int, image: RoomImageInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(RoomImage).filter(RoomImage.id == image_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in image.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Room image updated'}

@room_image_router.delete('/{image_id}', response_model=dict)
async def room_image_delete(image_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(RoomImage).filter(RoomImage.id == image_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Room image deleted'}