from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL= os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    symbol= Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    order_type = Column(String)

Base.metadata.create_all(bind=engine)

class OrderCreate(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/orders/")
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.post("/orders/")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order