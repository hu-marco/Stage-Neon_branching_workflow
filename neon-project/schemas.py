from pydantic import BaseModel


class CouponSchema(BaseModel):
    code: str
    discount: float
