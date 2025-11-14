import sys
import os
from datetime import datetime, timedelta
from app.models.database import Booking  # Add this import


# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.database import SessionLocal, Base, engine, Bus, User
from app.services.auth import get_password_hash

def init_database():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Clear existing buses and users (for clean restart)
        db.query(Booking).delete()
        db.query(Bus).delete()
        db.query(User).delete()
        
        # Add sample buses with more variety
        sample_buses = [
            Bus(
                bus_number="BUS001",
                route_name="Mumbai-Pune Express",
                source="Mumbai",
                destination="Pune",
                total_seats=50,
                available_seats=50,
                departure_time=datetime.utcnow() + timedelta(days=1),
                arrival_time=datetime.utcnow() + timedelta(days=1, hours=4),
                base_price=500.00
            ),
            Bus(
                bus_number="BUS002", 
                route_name="Delhi-Jaipur Superfast",
                source="Delhi",
                destination="Jaipur", 
                total_seats=45,
                available_seats=45,
                departure_time=datetime.utcnow() + timedelta(days=1),
                arrival_time=datetime.utcnow() + timedelta(days=1, hours=5),
                base_price=700.00
            ),
            Bus(
                bus_number="BUS003",
                route_name="Bangalore-Chennai AC",
                source="Bangalore", 
                destination="Chennai",
                total_seats=40,
                available_seats=40,
                departure_time=datetime.utcnow() + timedelta(days=1),
                arrival_time=datetime.utcnow() + timedelta(days=1, hours=6),
                base_price=800.00
            ),
            Bus(
                bus_number="BUS004",
                route_name="Hyderabad-Bangalore Sleeper",
                source="Hyderabad",
                destination="Bangalore",
                total_seats=35,
                available_seats=35,
                departure_time=datetime.utcnow() + timedelta(days=2),
                arrival_time=datetime.utcnow() + timedelta(days=2, hours=7),
                base_price=900.00
            ),
            Bus(
                bus_number="BUS005",
                route_name="Mumbai-Goa Luxury",
                source="Mumbai",
                destination="Goa",
                total_seats=30,
                available_seats=30,
                departure_time=datetime.utcnow() + timedelta(days=3),
                arrival_time=datetime.utcnow() + timedelta(days=3, hours=12),
                base_price=1200.00
            )
        ]
        
        db.add_all(sample_buses)
        
        # Create admin user
        admin_user = User(
            email="admin@bus.com",
            hashed_password=get_password_hash("admin123"),
            full_name="System Administrator",
            phone_number="+1234567890"
        )
        db.add(admin_user)
        
        # Create test user
        test_user = User(
            email="user@test.com",
            hashed_password=get_password_hash("user123"),
            full_name="Test User",
            phone_number="+0987654321"
        )
        db.add(test_user)
        
        db.commit()
        print("✅ Sample buses and users added to database!")
        print("🚌 Available routes:")
        for bus in sample_buses:
            print(f"   - {bus.source} → {bus.destination} ({bus.bus_number})")
            
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Initializing Bus Pass System Database...")
    init_database()
    print("🎉 Database initialization completed!")
    print("\n🔑 Test Credentials:")
    print("   Admin: admin@bus.com / admin123")
    print("   User:  user@test.com / user123")