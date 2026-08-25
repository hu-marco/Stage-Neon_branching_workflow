from datetime import date
from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    name : str
    email : str

class UserSchema(BaseModel):
    id : int
    name : str
    email : str
    
    model_config = {
    "from_attributes": True
    }

class ProductCreateSchema(BaseModel):
    name : str
    price : float
    stock : int

class ProductSchema(BaseModel):
    id : int
    name : str
    price : float
    stock : int

class CouponCreateSchema(BaseModel):
    code: str
    discount: float 
    
class CouponSchema(BaseModel):
    id : int
    code: str
    discount: float

class OrderCreateSchema(BaseModel):
    user_id : int
    created_at : date
    coupon_id : int | None = None
   

class OrderSchema(BaseModel):
    id : int
    user_id : int
    created_at : date
    coupon_id : int | None = None
    
    model_config = {
    "from_attributes": True
    }

class OrderItemCreateSchema(BaseModel):
    order_id : int
    product_id : int
    quantity :int 

class OrderItemSchema(BaseModel):
    id : int
    order_id : int
    product_id : int
    quantity :int 

class CategoryCreateSchema(BaseModel):
    name : str

class CategorySchema(BaseModel):
    id : int
    name : str

class AddressCreateSchema(BaseModel):
    user_id : int
    city : str
    street : str
    
class AddressSchema(BaseModel):
    id : int
    user_id : int
    city : str
    street : str