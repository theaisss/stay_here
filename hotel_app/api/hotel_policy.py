from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import HotelPolicy
from hotel_app.database.schema import HotelPolicyInputSchema, HotelPolicyOutSchema
from hotel_app.database.db import SessionLocal

policy_router = APIRouter(prefix='/hotel-policies', tags=['Hotel Policy CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@policy_router.post('/', response_model=HotelPolicyOutSchema)
async def policy_create(policy: HotelPolicyInputSchema, db: Session = Depends(get_db)):
    db_obj = HotelPolicy(**policy.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@policy_router.get('/', response_model=List[HotelPolicyOutSchema])
async def policy_list(db: Session = Depends(get_db)):
    return db.query(HotelPolicy).all()

@policy_router.get('/{policy_id}', response_model=HotelPolicyOutSchema)
async def policy_detail(policy_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(HotelPolicy).filter(HotelPolicy.id == policy_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@policy_router.put('/{policy_id}', response_model=dict)
async def policy_update(policy_id: int, policy: HotelPolicyInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(HotelPolicy).filter(HotelPolicy.id == policy_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in policy.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Hotel policy updated'}

@policy_router.delete('/{policy_id}', response_model=dict)
async def policy_delete(policy_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(HotelPolicy).filter(HotelPolicy.id == policy_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Hotel policy deleted'}