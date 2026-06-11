from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import Country
from hotel_app.database.schema import CountryInputSchema, CountryOutSchema
from hotel_app.database.db import SessionLocal

country_router = APIRouter(prefix='/countries', tags=['Country CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@country_router.post('/', response_model=CountryOutSchema)
async def country_create(country: CountryInputSchema, db: Session = Depends(get_db)):
    db_obj = Country(**country.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@country_router.get('/', response_model=List[CountryOutSchema])
async def country_list(db: Session = Depends(get_db)):
    return db.query(Country).all()

@country_router.get('/{country_id}', response_model=CountryOutSchema)
async def country_detail(country_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Country).filter(Country.id == country_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@country_router.put('/{country_id}', response_model=dict)
async def country_update(country_id: int, country: CountryInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(Country).filter(Country.id == country_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in country.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Country updated'}

@country_router.delete('/{country_id}', response_model=dict)
async def country_delete(country_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Country).filter(Country.id == country_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Country deleted'}