from pydantic import BaseModel

class OrderCreate(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

class OrderResponse(BaseModel):
    id: int
    symbol: str
    price: float
    quantity: int
    order_type: str

    class Config:
        from_attributes = True