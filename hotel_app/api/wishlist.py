from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import Wishlist
from hotel_app.database.schema import (WishlistInputSchema, WishlistOutSchema)
from hotel_app.database.db import SessionLocal

wishlist_router = APIRouter(prefix='/wishlists', tags=['Wishlist CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@wishlist_router.post('/', response_model=WishlistOutSchema)
async def wishlist_create(wishlist: WishlistInputSchema, db: Session = Depends(get_db)):
    db_obj = Wishlist(**wishlist.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@wishlist_router.get('/', response_model=List[WishlistOutSchema])
async def wishlist_list(db: Session = Depends(get_db)):
    return db.query(Wishlist).all()

@wishlist_router.get('/{wishlist_id}', response_model=WishlistOutSchema)
async def wishlist_detail(wishlist_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@wishlist_router.put('/{wishlist_id}', response_model=dict)
async def wishlist_update(wishlist_id: int, wishlist: WishlistInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in wishlist.model_dump().items():
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Wishlist updated'}

@wishlist_router.delete('/{wishlist_id}', response_model=dict)
async def wishlist_delete(wishlist_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Wishlist).filter(Wishlist.id == wishlist_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Wishlist deleted'}