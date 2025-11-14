from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import redis
import json
import uuid
from datetime import datetime, timedelta

from .models.database import SessionLocal, engine, Base
from .models.schemas import (
    UserCreate, UserResponse, BusCreate, BusResponse, 
    BookingCreate, BookingResponse, TicketResponse
)
from .services.auth import get_current_user, create_access_token, verify_password, get_password_hash
from .services.booking_service import BookingService
from .services.pricing_service import PricingService
from .services.qr_service import QRService
from .routes import users, buses, bookings, auth

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud Bus Pass System",
    description="Scalable cloud-based bus ticket booking system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis connection for caching and rate limiting
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(buses.router, prefix="/api/v1/buses", tags=["buses"])
app.include_router(bookings.router, prefix="/api/v1/bookings", tags=["bookings"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Cloud Bus Pass System API", "status": "healthy"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)