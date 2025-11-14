CREATE DATABASE IF NOT EXISTS bus_system;
USE bus_system;

-- Users table already created by SQLAlchemy
-- Insert sample buses
INSERT INTO buses (bus_number, route_name, source, destination, total_seats, available_seats, departure_time, arrival_time, base_price) VALUES
('BUS001', 'Mumbai - Pune Express', 'Mumbai', 'Pune', 50, 50, '2024-01-20 08:00:00', '2024-01-20 12:00:00', 500.00),
('BUS002', 'Delhi - Jaipur Superfast', 'Delhi', 'Jaipur', 45, 45, '2024-01-20 09:00:00', '2024-01-20 14:00:00', 700.00),
('BUS003', 'Bangalore - Chennai AC', 'Bangalore', 'Chennai', 40, 40, '2024-01-20 10:00:00', '2024-01-20 16:00:00', 800.00);