from fastapi import APIRouter, Depends
import os
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date

import database as db
from models import Order
from schemas import OrderSchema

router = APIRouter()

@router.get("/get_orders_by_date", response_model=list[OrderSchema])
def get_orders_by_date(created_at_from:str, db: Session = Depends(db.get_db)):
    
    date_from= date.fromisoformat(created_at_from)
    
    orders = db.execute(
        select(Order)
        .where(Order.created_at >= date_from)
    ).scalars().all()
    
    return orders
