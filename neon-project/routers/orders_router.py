from fastapi import APIRouter, Depends,  HTTPException
import os
from sqlalchemy.orm import Session
from sqlalchemy import select, text
from datetime import date

import database as db
from models import Order
from schemas import OrderSchema, OrderCreateSchema

router = APIRouter(prefix="/orders")

@router.get("/get_orders_by_date", response_model=list[OrderSchema])
def get_orders_by_date(created_at_from:str, db: Session = Depends(db.get_db)):
    
    date_from= date.fromisoformat(created_at_from)
    
    orders = db.execute(
        select(Order)
        .where(Order.created_at >= date_from)
    ).scalars().all()
    
    return orders

@router.get("/get_order_by_id", response_model=OrderSchema)
def get_order_by_id(order_id:int, db: Session = Depends(db.get_db)):
    order = db.execute(
        select(Order)
        .where(Order.id == order_id)
    ).scalar_one_or_none()
    
    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )
    
    return order

@router.post("/create_order")
def create_order(order: OrderCreateSchema, db: Session = Depends(db.get_db)):
    new_order = Order(
        user_id= order.user_id,
        created_at= order.created_at
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {
        "status": "created",
        "id": new_order.id
    }
    
    
@router.patch("/set_coupon")
def set_coupon_id(order_id:int, coupon_id:int, db: Session = Depends(db.get_db)):
    result = db.execute(
        text("""
            UPDATE orders
            SET coupon_id = :coupon_id
            WHERE id = :order_id
        """),
        {
            "coupon_id": coupon_id,
            "order_id": order_id
        }
    )

    db.commit()
    if result.rowcount == 0:
        return {"status": "error", "message": "Operation failed"}
        
    return {
        "status": "success",
        "message": "Coupon added to the order"
    }


@router.patch("/calculate_total")
def calculate_total(order_id:int, db: Session = Depends(db.get_db)):
    result = db.execute(
        text("""
            UPDATE orders
            SET total_price = COALESCE((
            SELECT SUM(p.price * o.quantity)
            from products p INNER JOIN  order_items o 
            ON p.id = o.product_id
            WHERE orders.id= o.order_id),0)
            WHERE orders.id= :order_id;
        """),
        {
            "order_id": order_id
        }
    )
    db.commit()
    if result.rowcount == 0:
        return {"status": "error", "message": "Operation failed"}
    
    return {
        "status": "success",
        "message": "Total price was calculated"
    }

@router.get("/get_total_price")
def get_total_price(order_id:int, db: Session = Depends(db.get_db)):
    result = db.execute(
        text("""
            select total_price
            from orders
            where id= :order_id;
        """),
        {
            "order_id": order_id
        }
    )
    
    total_price = result.scalar_one_or_none()
    
    if total_price is None:
        raise HTTPException(
            status_code=404,
            detail="Total price not found"
        )
    return {
        "status": "success",
        "total_price": total_price
    }
    


@router.patch("/apply_discount")
def apply_discount(order_id:int, db: Session = Depends(db.get_db)):    
    result = db.execute(
        text("""
            UPDATE orders
            SET total_price = total_price * (
                1 - (
                    SELECT discount
                    FROM coupons c
                    WHERE c.id = orders.coupon_id
                ) / 100.0
            )
            WHERE id = :order_id
              AND coupon_id IS NOT NULL
        """),
        {"order_id": order_id}
    )
    db.commit()
    if result.rowcount == 0:
        return {"status": "error", "message": "Operation failed"}
    
    return {
        "status": "success",
        "message": "Discount was applied"
    }

@router.get("/get_orders_by_user_id", response_model=list[OrderSchema])
def get_orders_by_user_id(user_id:int, db: Session = Depends(db.get_db)):
    
    orders = db.execute(
        select(Order)
        .where(Order.user_id == user_id)
    ).scalars().all()
    
    return orders
    
    

@router.get("/get_orders_by_100", response_model=list[OrderSchema])
def get_orders_by_100(page: int, user_id:int ,db: Session = Depends(db.get_db)):
    offset = (page - 1) * 100
    orders = (
        db.query(Order)
        .where(Order.user_id == user_id)
        .order_by(Order.id)
        .offset(offset)
        .limit(100)
        .all()
    )

    return orders
