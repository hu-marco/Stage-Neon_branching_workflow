from fastapi import APIRouter, Depends
import os
from sqlalchemy.orm import Session

from schemas import CouponCreateSchema
import database as db
from models import Coupon

router = APIRouter()

@router.post("/create_coupon")
def create_coupon(coupon: CouponCreateSchema, db: Session = Depends(db.get_db)):
    new_coupon = Coupon(
        code=coupon.code,
        discount=coupon.discount
    )

    db.add(new_coupon)
    db.commit()
    db.refresh(new_coupon)
    return {
        "status": "created",
        "id": new_coupon.id
    }
