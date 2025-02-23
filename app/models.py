from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    order_type = Column(String)