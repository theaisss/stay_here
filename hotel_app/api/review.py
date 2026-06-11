from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import Review
from hotel_app.database.schema import ReviewInputSchema, ReviewOutSchema
from hotel_app.database.db import SessionLocal

review_router = APIRouter(prefix='/reviews', tags=['Review CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@review_router.post('/', response_model=ReviewOutSchema)
async def review_create(review: ReviewInputSchema, db: Session = Depends(get_db)):
    db_obj = Review(**review.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@review_router.get('/', response_model=List[ReviewOutSchema])
async def review_list(db: Session = Depends(get_db)):
    return db.query(Review).all()

@review_router.get('/{review_id}', response_model=ReviewOutSchema)
async def review_detail(review_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Review).filter(Review.id == review_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@review_router.put('/{review_id}', response_model=dict)
async def review_update(review_id: int, review: ReviewInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(Review).filter(Review.id == review_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in review.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Review updated'}

@review_router.delete('/{review_id}', response_model=dict)
async def review_delete(review_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Review).filter(Review.id == review_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Review deleted'}