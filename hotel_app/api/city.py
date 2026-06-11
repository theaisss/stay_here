from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import City
from hotel_app.database.schema import CityInputSchema, CityOutSchema
from hotel_app.database.db import SessionLocal

city_router = APIRouter(prefix='/cities', tags=['City CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@city_router.post('/', response_model=CityOutSchema)
async def city_create(city: CityInputSchema, db: Session = Depends(get_db)):
    db_obj = City(**city.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@city_router.get('/', response_model=List[CityOutSchema])
async def city_list(db: Session = Depends(get_db)):
    return db.query(City).all()

@city_router.get('/{city_id}', response_model=CityOutSchema)
async def city_detail(city_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(City).filter(City.id == city_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@city_router.put('/{city_id}', response_model=dict)
async def city_update(city_id: int, city: CityInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(City).filter(City.id == city_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in city.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'City updated'}

@city_router.delete('/{city_id}', response_model=dict)
async def city_delete(city_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(City).filter(City.id == city_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'City deleted'}