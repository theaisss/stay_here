from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from hotel_app.database.models import Payment, PaymentMethodChoices, PaymentStatusChoices
from hotel_app.database.schema import PaymentInputSchema, PaymentOutSchema
from hotel_app.database.db import SessionLocal

payment_router = APIRouter(prefix='/payments', tags=['Payment CRUD'])

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@payment_router.post('/', response_model=PaymentOutSchema)
async def payment_create(payment: PaymentInputSchema, db: Session = Depends(get_db)):
    data = payment.model_dump()
    if 'method' in data:
        data['method'] = PaymentMethodChoices(data['method'])
    if 'status' in data:
        data['status'] = PaymentStatusChoices(data['status'])
    db_obj = Payment(**data)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@payment_router.get('/', response_model=List[PaymentOutSchema])
async def payment_list(db: Session = Depends(get_db)):
    return db.query(Payment).all()

@payment_router.get('/{payment_id}', response_model=PaymentOutSchema)
async def payment_detail(payment_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    return db_obj

@payment_router.put('/{payment_id}', response_model=dict)
async def payment_update(payment_id: int, payment: PaymentInputSchema, db: Session = Depends(get_db)):
    db_obj = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    for key, value in payment.model_dump().items():
        if key == 'method' and value is not None:
            value = PaymentMethodChoices(value)
        elif key == 'status' and value is not None:
            value = PaymentStatusChoices(value)
        setattr(db_obj, key, value)
    db.commit()
    return {'message': 'Payment updated'}

@payment_router.delete('/{payment_id}', response_model=dict)
async def payment_delete(payment_id: int, db: Session = Depends(get_db)):
    db_obj = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_obj:
        raise HTTPException(detail='Information not found', status_code=404)
    db.delete(db_obj)
    db.commit()
    return {'message': 'Payment deleted'}