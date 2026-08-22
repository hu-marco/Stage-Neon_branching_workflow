from sqlalchemy import Column, Integer, Numeric, String, ForeignKey , Date
from database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    

class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price= Column(Numeric)
    stock = Column(Integer)


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(Date)
    
    coupon_id = Column(Integer,  ForeignKey("coupons.id"), nullable=True)


class OrderItem(Base):

    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
  
class Address(Base):

    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String)
    street = Column(String)


class Coupon(Base):

    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    discount = Column(Integer)
