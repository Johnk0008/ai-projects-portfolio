from sqlalchemy.orm import Session
from datetime import datetime
import uuid
import redis
from ..models.database import Bus, Booking, User
from ..models.schemas import BookingCreate
from .pricing_service import PricingService
from .qr_service import QRService

class BookingService:
    def __init__(self, db: Session):
        self.db = db
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.pricing_service = PricingService()
        self.qr_service = QRService()

    def create_booking(self, booking_data: BookingCreate, user_id: int):
        # Check bus availability with distributed lock
        bus = self.db.query(Bus).filter(Bus.id == booking_data.bus_id, Bus.is_active == True).first()
        if not bus:
            raise ValueError("Bus not found")
        
        # Acquire lock for seat reservation
        lock_key = f"bus_lock:{bus.id}"
        if not self.redis_client.set(lock_key, "locked", nx=True, ex=10):
            raise ValueError("Seat reservation in progress, please try again")
        
        try:
            if bus.available_seats < booking_data.seats_booked:
                raise ValueError("Not enough seats available")
            
            # Calculate dynamic pricing
            total_amount = self.pricing_service.calculate_price(
                bus.base_price, 
                booking_data.seats_booked,
                bus.available_seats,
                bus.total_seats
            )
            
            # Generate unique references
            booking_reference = f"BR{datetime.utcnow().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
            ticket_number = f"TKT{uuid.uuid4().hex[:12].upper()}"
            
            # Create booking
            booking = Booking(
                user_id=user_id,
                bus_id=booking_data.bus_id,
                seats_booked=booking_data.seats_booked,
                total_amount=total_amount,
                booking_reference=booking_reference,
                ticket_number=ticket_number,
                booking_status="confirmed"
            )
            
            # Update available seats
            bus.available_seats -= booking_data.seats_booked
            
            # Generate QR code
            qr_data = self.qr_service.generate_qr_code({
                "ticket_number": ticket_number,
                "booking_reference": booking_reference,
                "bus_number": bus.bus_number,
                "seats": booking_data.seats_booked,
                "timestamp": datetime.utcnow().isoformat()
            })
            booking.qr_code_data = qr_data
            
            self.db.add(booking)
            self.db.commit()
            self.db.refresh(booking)
            
            # Cache booking data
            booking_cache_key = f"booking:{booking_reference}"
            self.redis_client.setex(
                booking_cache_key, 
                3600,  # 1 hour cache
                f"{booking_reference}:{ticket_number}:confirmed"
            )
            
            return booking
            
        finally:
            # Release lock
            self.redis_client.delete(lock_key)

    def get_booking_by_reference(self, booking_reference: str):
        # Try cache first
        cache_key = f"booking:{booking_reference}"
        cached_data = self.redis_client.get(cache_key)
        
        if cached_data:
            return cached_data
        
        # Database lookup
        booking = self.db.query(Booking).filter(Booking.booking_reference == booking_reference).first()
        if booking:
            # Cache the result
            self.redis_client.setex(cache_key, 3600, f"{booking.booking_reference}:{booking.ticket_number}:{booking.booking_status}")
            return booking
        
        return None