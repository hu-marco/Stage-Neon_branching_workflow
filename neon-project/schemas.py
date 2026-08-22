from datetime import date
from pydantic import BaseModel


class UserSchema(BaseModel):
    name : str
    email : str

class ProductSchema(BaseModel):
    name : str
    price : float
    stock : int


class CouponSchema(BaseModel):
    code: str
    discount: float
    

class OrderSchema(BaseModel):
    user_id : int
    created_at : date
    coupon_id : int | None = None
    
    model_config = {
    "from_attributes": True
    }

class OrderItemSchema(BaseModel):
    order_id : int
    product_id : int
    quantity :int 


class CategorySchema(BaseModel):
    name : str
    
class Address(BaseModel):
    user_id : int
    city : str
    street : str