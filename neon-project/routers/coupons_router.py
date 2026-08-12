from fastapi import APIRouter, Depends
import database as db
import os

router = APIRouter()

@router.post("/create_coupon")
def create_coupon(coupon: CouponSchema, db: Session = Depends(get_db)):
    new_coupon = Coupon(
        code=coupon.code,
        discount=coupon.discount
    )

    db.add(new_coupon)
    db.commit()
    return {"status": "created"}
