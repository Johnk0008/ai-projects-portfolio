import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.database import SessionLocal, Bus

def check_buses():
    db = SessionLocal()
    try:
        buses = db.query(Bus).all()
        print("🚌 Available Buses in Database:")
        print("-" * 50)
        for bus in buses:
            print(f"ID: {bus.id}")
            print(f"Bus Number: {bus.bus_number}")
            print(f"Route: {bus.route_name}")
            print(f"From: {bus.source} → To: {bus.destination}")
            print(f"Seats: {bus.available_seats}/{bus.total_seats}")
            print(f"Departure: {bus.departure_time}")
            print("-" * 30)
        
        if not buses:
            print("❌ No buses found in database!")
            print("Run: python init_db.py")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_buses()