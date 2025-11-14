from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class BusBase(BaseModel):
    bus_number: str
    route_name: str
    source: str
    destination: str
    total_seats: int
    departure_time: datetime
    arrival_time: datetime
    base_price: float

class BusCreate(BusBase):
    pass

class BusResponse(BusBase):
    id: int
    available_seats: int
    is_active: bool
    
    class Config:
        from_attributes = True

class BookingBase(BaseModel):
    bus_id: int
    seats_booked: int

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: int
    user_id: int
    total_amount: float
    booking_reference: str
    ticket_number: str
    booking_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TicketResponse(BookingResponse):
    qr_code_data: str
    bus_details: BusResponse
    user_details: UserResponse
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None