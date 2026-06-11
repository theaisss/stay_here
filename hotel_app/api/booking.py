from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import Booking, BookingStatusChoices
from hotel_app.database.schema import BookingInputSchema, BookingOutSchema
from hotel_app.database.db import SessionLocal

booking_router = APIRouter(prefix='/bookings', tags=['Booking CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@booking_router.post('/', response_model=BookingOutSchema)
async def booking_create(booking: BookingInputSchema, db: Session = Depends(get_db)):
    data = booking.model_dump()
    if 'status' in data:
        data['status'] = BookingStatusChoices(data['status'])
    db_obj = Booking(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@booking_router.get('/', response_model=List[BookingOutSchema])
async def booking_list(db: Session = Depends(get_db)):
    return db.query(Booking).all()

@booking_router.get('/{booking_id}', response_model=BookingOutSchema)
async def booking_detail(booking_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@booking_router.put('/{booking_id}', response_model=dict)
async def booking_update(booking_id: int, booking: BookingInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in booking.model_dump().items():
        if key == 'status' and value is not None:
            value = BookingStatusChoices(value)
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Booking updated'}

@booking_router.delete('/{booking_id}', response_model=dict)
async def booking_delete(booking_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Booking deleted'}