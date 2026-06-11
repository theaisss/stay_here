from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import Hotel
from hotel_app.database.schema import HotelInputSchema, HotelOutSchema
from hotel_app.database.db import SessionLocal

hotel_router = APIRouter(prefix='/hotels', tags=['Hotel CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@hotel_router.post('/', response_model=HotelOutSchema)
async def hotel_create(hotel: HotelInputSchema, db: Session = Depends(get_db)):
    db_obj = Hotel(**hotel.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@hotel_router.get('/', response_model=List[HotelOutSchema])
async def hotel_list(db: Session = Depends(get_db)):
    return db.query(Hotel).all()

@hotel_router.get('/{hotel_id}', response_model=HotelOutSchema)
async def hotel_detail(hotel_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@hotel_router.put('/{hotel_id}', response_model=dict)
async def hotel_update(hotel_id: int, hotel: HotelInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in hotel.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Hotel updated'}

@hotel_router.delete('/{hotel_id}', response_model=dict)
async def hotel_delete(hotel_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Hotel deleted'}