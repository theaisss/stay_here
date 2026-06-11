from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import HotelImage
from hotel_app.database.schema import HotelImageInputSchema, HotelImageOutSchema
from hotel_app.database.db import SessionLocal

hotel_image_router = APIRouter(prefix='/hotel-images', tags=['Hotel Image CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@hotel_image_router.post('/', response_model=HotelImageOutSchema)
async def hotel_image_create(image: HotelImageInputSchema, db: Session = Depends(get_db)):
    db_obj = HotelImage(**image.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@hotel_image_router.get('/', response_model=List[HotelImageOutSchema])
async def hotel_image_list(db: Session = Depends(get_db)):
    return db.query(HotelImage).all()

@hotel_image_router.get('/{image_id}', response_model=HotelImageOutSchema)
async def hotel_image_detail(image_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(HotelImage).filter(HotelImage.id == image_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@hotel_image_router.put('/{image_id}', response_model=dict)
async def hotel_image_update(image_id: int, image: HotelImageInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(HotelImage).filter(HotelImage.id == image_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in image.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Hotel image updated'}

@hotel_image_router.delete('/{image_id}', response_model=dict)
async def hotel_image_delete(image_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(HotelImage).filter(HotelImage.id == image_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Hotel image deleted'}