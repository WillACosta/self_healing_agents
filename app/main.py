from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, init_db, Plant, Order
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from database import engine
import time
import random

app = FastAPI(title="Fake Plant Shop API")

# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    init_db()

# Instrument FastAPI with Prometheus
Instrumentator().instrument(app).expose(app)

# Instrument FastAPI and SQLAlchemy with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)
SQLAlchemyInstrumentor().instrument(engine=engine)

@app.get("/plants", tags=["Store"], summary="List all available plants")
def list_plants(db: Session = Depends(get_db)):
    """
    Retrieve a list of all plants in the shop.
    Note: This endpoint has a simulated performance bottleneck.
    """
    # Issue 2/3: N+1-like issue or slow serialization
    # In this case, we'll simulate a slow operation for each plant found
    plants = db.query(Plant).all()

    result = []
    for plant in plants:
        # Simulating heavy processing or a hidden secondary query for each item
        time.sleep(0.05)
        result.append({
            "id": plant.id,
            "name": plant.name,
            "price": plant.price,
            "stock": plant.stock,
            "description": plant.description
        })

    return result

@app.post("/checkout", tags=["Orders"], summary="Place a new order")
def checkout(plant_id: int, quantity: int, db: Session = Depends(get_db)):
    """
    Purchase a plant from the shop.
    Note: This endpoint has a 30% chance of high latency.
    """
    # Issue 3/3: Random slow checkout / inefficient lock simulation
    # Sometimes checkout is very slow due to "external validation" or bad logic
    if random.random() < 0.3: # 30% chance of being slow
        time.sleep(2.0)

    plant = db.query(Plant).filter(Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    if plant.stock < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    plant.stock -= quantity
    order = Order(plant_id=plant_id, quantity=quantity, total_price=plant.price * quantity)
    db.add(order)
    db.commit()

    return {"message": "Order placed successfully", "order_id": order.id}

@app.get("/health", tags=["System"], summary="Health check")
def health_check():
    return {"status": "healthy"}

