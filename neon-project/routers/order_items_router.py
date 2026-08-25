from fastapi import APIRouter, Depends
import os
from sqlalchemy.orm import Session

from schemas import OrderItemSchema, OrderItemCreateSchema
import database as db
from models import OrderItem

router = APIRouter()

@router.post("/create_order_item")
def create_coupon(order_item: OrderItemCreateSchema, db: Session = Depends(db.get_db)):
    new_order_item = OrderItem(
        order_id = order_item.order_id,
        product_id = order_item.product_id,
        quantity = order_item.quantity
    )
    
    db.add(new_order_item)
    db.commit()
    db.refresh(new_order_item)
    return {
        "status": "created",
        "id": new_order_item.id
    }
