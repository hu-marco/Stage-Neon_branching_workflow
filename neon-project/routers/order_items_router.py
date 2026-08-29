from fastapi import APIRouter, Depends
import os
from sqlalchemy.orm import Session

from schemas import OrderItemSchema, OrderItemCreateSchema
import database as db
from models import OrderItem

router = APIRouter(prefix="/order_items")

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

@router.get("/get_order_items_by_order_id", response_model=list[OrderItemSchema])
def get_order_items_by_order_id(order_id: int ,db: Session = Depends(db.get_db)):
    
    order_items = db.execute(
        select(OrderItem)
        .where(OrderItem.order_id == order_id)
    ).scalars().all()

    return order_items


@router.get("/get_order_items_by_100", response_model=list[OrderItemSchema])
def get_order_items_by_100(page: int , order_id:int, db: Session = Depends(db.get_db)):
    offset = (page - 1) * 100
    products = (
        db.query(OrderItem)
        .where(OrderItem.order_id== order_id)
        .order_by(OrderItem.id)
        .offset(offset)
        .limit(100)
        .all()
    )

    return products
