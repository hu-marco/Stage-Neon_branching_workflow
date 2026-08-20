from fastapi import APIRouter, Depends
import os
from sqlalchemy.orm import Session
from schemas import CouponSchema
import database as db
from models import Coupon

router = APIRouter()

@router.post("/create_coupon")
def create_coupon(coupon: CouponSchema, db: Session = Depends(db.get_db)):
    new_coupon = Coupon(
        code=coupon.code,
        discount=coupon.discount
    )

    db.add(new_coupon)
    db.commit()
    return {"status": "created"}
