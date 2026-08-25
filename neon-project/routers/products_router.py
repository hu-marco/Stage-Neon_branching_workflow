from fastapi import APIRouter, Depends
import os
from sqlalchemy.orm import Session

from schemas import ProductSchema, ProductCreateSchema 
import database as db
from models import Product

router = APIRouter()

@router.post("/create_product")
def create_coupon(product: ProductCreateSchema, db: Session = Depends(db.get_db)):
    new_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock    
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "status": "created",
        "id": new_product.id
    }
