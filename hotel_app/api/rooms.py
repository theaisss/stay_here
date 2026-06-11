from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import Room, RoomTypeChoices
from hotel_app.database.schema import RoomInputSchema, RoomOutSchema
from hotel_app.database.db import SessionLocal

room_router = APIRouter(prefix='/rooms', tags=['Room CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@room_router.post('/', response_model=RoomOutSchema)
async def room_create(room: RoomInputSchema, db: Session = Depends(get_db)):
    data = room.model_dump()
    if 'room_type' in data:
        data['room_type'] = RoomTypeChoices(data['room_type'])
    db_obj = Room(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@room_router.get('/', response_model=List[RoomOutSchema])
async def room_list(db: Session = Depends(get_db)):
    return db.query(Room).all()

@room_router.get('/{room_id}', response_model=RoomOutSchema)
async def room_detail(room_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Room).filter(Room.id == room_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@room_router.put('/{room_id}', response_model=dict)
async def room_update(room_id: int, room: RoomInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(Room).filter(Room.id == room_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in room.model_dump().items():
        if key == 'room_type' and value is not None:
            value = RoomTypeChoices(value)
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Room updated'}

@room_router.delete('/{room_id}', response_model=dict)
async def room_delete(room_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Room).filter(Room.id == room_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Room deleted'}