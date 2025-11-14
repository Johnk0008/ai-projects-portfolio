from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..models.database import SessionLocal, Bus, User
from ..models.schemas import BusResponse, BusCreate
from ..services.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[BusResponse])
async def get_buses(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    buses = db.query(Bus).filter(Bus.is_active == True).offset(skip).limit(limit).all()
    return buses

@router.get("/{bus_id}", response_model=BusResponse)
async def get_bus(bus_id: int, db: Session = Depends(get_db)):
    bus = db.query(Bus).filter(Bus.id == bus_id, Bus.is_active == True).first()
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")
    return bus

@router.post("/", response_model=BusResponse)
async def create_bus(bus: BusCreate, db: Session = Depends(get_db)):
    # Check if bus number already exists
    existing_bus = db.query(Bus).filter(Bus.bus_number == bus.bus_number).first()
    if existing_bus:
        raise HTTPException(status_code=400, detail="Bus number already exists")
    
    db_bus = Bus(
        bus_number=bus.bus_number,
        route_name=bus.route_name,
        source=bus.source,
        destination=bus.destination,
        total_seats=bus.total_seats,
        available_seats=bus.total_seats,  # Initially all seats available
        departure_time=bus.departure_time,
        arrival_time=bus.arrival_time,
        base_price=bus.base_price
    )
    
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    return db_bus