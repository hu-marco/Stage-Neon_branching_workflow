from fastapi import APIRouter, Depends
import os
from sqlalchemy.orm import Session, select
from datetime import datetime
import database as db
from models import Order
from schemas import OrderSchema

router = APIRouter()

@router.get("/get_orders_by_date", response_model=list[OrderSchema])
def get_orders_by_date(created_at_from:str):
    
    date= datetime.fromisoformat(created_at_from)

    orders = session.execute(
        select(Order)
        .where(Order.idx_orders_created >= date_from)
    ).scalars().all()

    return orders
