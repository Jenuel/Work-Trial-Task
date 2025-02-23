from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .models import Order
from .schemas import OrderCreate, OrderResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

#GET /orders/ - Fetch all orders
@app.get("/orders/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.post("/orders/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = Order(**order.model_dump())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order