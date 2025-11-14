from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models.database import SessionLocal, Booking, User, Bus
from ..models.schemas import BookingResponse, BookingCreate, TicketResponse
from ..services.auth import get_current_user
from ..services.booking_service import BookingService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BookingResponse)
async def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking_service = BookingService(db)
    try:
        new_booking = booking_service.create_booking(booking, current_user.id)
        return new_booking
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-bookings", response_model=List[BookingResponse])
async def get_my_bookings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).all()
    return bookings

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.get("/{booking_id}/ticket", response_model=TicketResponse)
async def get_ticket(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    booking = db.query(Booking).filter(
        Booking.id == booking_id, 
        Booking.user_id == current_user.id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    # Convert to TicketResponse with additional details
    ticket_data = {
        "id": booking.id,
        "bus_id": booking.bus_id,
        "seats_booked": booking.seats_booked,
        "user_id": booking.user_id,
        "total_amount": booking.total_amount,
        "booking_reference": booking.booking_reference,
        "ticket_number": booking.ticket_number,
        "booking_status": booking.booking_status,
        "created_at": booking.created_at,
        "qr_code_data": booking.qr_code_data,
        "bus_details": booking.bus,
        "user_details": booking.user
    }
    return TicketResponse(**ticket_data)