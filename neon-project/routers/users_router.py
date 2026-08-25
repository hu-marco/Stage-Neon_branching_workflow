from fastapi import APIRouter, Depends, HTTPException
import os
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date

import database as db
from models import User
from schemas import UserSchema

router = APIRouter()

@router.get("/login", response_model=UserSchema)
def get_orders_by_date(email_address:str, db: Session = Depends(db.get_db)):
    user = db.execute(
        select(User)
        .where(User.email == email_address)
    ).scalar_one_or_none()
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user