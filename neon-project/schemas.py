from datetime import datetime
from pydantic import BaseModel


class UserSchema(BaseModel):
    name : str
    email : str

class Product(Base):

    name : str
    price : float
    stock : int


class CouponSchema(BaseModel):
    code: str
    discount: float
    

class OrderSchema(BaseModel):
    user_id : int
    created_at : datetime    
    idx_orders_created : datetime
    coupon_code : str
    
    model_config = {
    "from_attributes": True
    }

class OrderItemSchema(Base):
    order_id : int
    product_id : int
    quantity :int 


class Category(Base):
    name : str
    
class Address(Base):

    user_id : int
    city : str
    street : str