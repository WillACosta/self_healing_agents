from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import time

DATABASE_URL = "sqlite:///./plants.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Plant(Base):
    __tablename__ = "plants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Integer, index=True)
    price = Column(Float)
    stock = Column(Integer)
    description = Column(String)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(Integer, ForeignKey("plants.id"))
    quantity = Column(Integer)
    total_price = Column(Float)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(Plant).count() == 0:
        # Issue 1/3: Slow data seeding (inefficient loop with multiple commits)
        # In a real app, this should be a bulk insert
        plants = [
            {"name": "Monstera", "price": 25.0, "stock": 10, "description": "Swiss Cheese Plant"},
            {"name": "Fiddle Leaf Fig", "price": 45.0, "stock": 5, "description": "Large indoor tree"},
            {"name": "Snake Plant", "price": 15.0, "stock": 20, "description": "Low maintenance"},
            {"name": "Pothos", "price": 10.0, "stock": 50, "description": "Easy to propagate"},
            {"name": "Succulent Mix", "price": 12.0, "stock": 30, "description": "Small and cute"}
        ]
        
        for plant_data in plants:
            plant = Plant(**plant_data)
            db.add(plant)
            db.commit() # Committing inside the loop is slow
            time.sleep(0.1) # Simulating extra latency in DB initialization
            
    db.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
