from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import Amenity
from hotel_app.database.schema import AmenityInputSchema, AmenityOutSchema
from ..database.db import SessionLocal

amenity_router = APIRouter(prefix='/amenities', tags=['Amenity CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@amenity_router.post('/', response_model=AmenityOutSchema)
async def amenity_create(amenity: AmenityInputSchema, db: Session = Depends(get_db)):
    db_obj = Amenity(**amenity.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@amenity_router.get('/', response_model=List[AmenityOutSchema])
async def amenity_list(db: Session = Depends(get_db)):
    return db.query(Amenity).all()

@amenity_router.get('/{amenity_id}', response_model=AmenityOutSchema)
async def amenity_detail(amenity_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@amenity_router.put('/{amenity_id}', response_model=dict)
async def amenity_update(amenity_id: int, amenity: AmenityInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in amenity.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Amenity updated'}

@amenity_router.delete('/{amenity_id}', response_model=dict)
async def amenity_delete(amenity_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Amenity).filter(Amenity.id == amenity_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Amenity deleted'}