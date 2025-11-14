from datetime import datetime, timedelta

class PricingService:
    def calculate_price(self, base_price: float, seats: int, available_seats: int, total_seats: int):
        """
        Calculate dynamic pricing based on:
        - Base price
        - Demand (available seats)
        - Time until departure
        - Number of seats booked
        """
        price = base_price * seats
        
        # Demand-based pricing (less seats = higher price)
        occupancy_rate = (total_seats - available_seats) / total_seats
        if occupancy_rate > 0.8:  # High demand
            price *= 1.2
        elif occupancy_rate > 0.5:  # Medium demand
            price *= 1.1
        
        # Bulk discount
        if seats >= 4:
            price *= 0.9  # 10% discount
        elif seats >= 2:
            price *= 0.95  # 5% discount
            
        return round(price, 2)