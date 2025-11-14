import streamlit as st
import requests
import json
from datetime import datetime, timedelta
import base64
import io
from PIL import Image

# API configuration
API_BASE_URL = "http://localhost:8000/api/v1"

def init_session_state():
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'user' not in st.session_state:
        st.session_state.user = None

def login():
    st.title("🚍 Cloud Bus Pass System - Login")
    
    with st.form("login_form"):
        email = st.text_input("Email", value="admin@bus.com")
        password = st.text_input("Password", type="password", value="admin123")
        submit = st.form_submit_button("Login")
        
        if submit:
            try:
                # Use form data for OAuth2 compatibility
                response = requests.post(
                    f"{API_BASE_URL}/auth/login",
                    data={"username": email, "password": password}
                )
                if response.status_code == 200:
                    token_data = response.json()
                    st.session_state.token = token_data['access_token']
                    
                    # Get user info
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    user_response = requests.get(f"{API_BASE_URL}/users/me", headers=headers)
                    
                    if user_response.status_code == 200:
                        st.session_state.user = user_response.json()
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Failed to get user information")
                else:
                    st.error("Login failed. Please check your credentials.")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server. Make sure the backend is running on http://localhost:8000")
            except Exception as e:
                st.error(f"Login error: {str(e)}")

def register():
    st.title("Create New Account")
    
    with st.form("register_form"):
        email = st.text_input("Email", placeholder="your@email.com")
        full_name = st.text_input("Full Name", placeholder="John Doe")
        phone = st.text_input("Phone Number", placeholder="+1234567890")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Register")
        
        if submit:
            if password != confirm_password:
                st.error("Passwords do not match!")
                return
                
            try:
                response = requests.post(
                    f"{API_BASE_URL}/auth/register",
                    json={
                        "email": email,
                        "full_name": full_name,
                        "phone_number": phone,
                        "password": password
                    }
                )
                if response.status_code == 200:
                    st.success("Registration successful! Please login.")
                else:
                    error_detail = response.json().get('detail', 'Unknown error')
                    st.error(f"Registration failed: {error_detail}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server. Make sure the backend is running on http://localhost:8000")
            except Exception as e:
                st.error(f"Registration error: {str(e)}")

def dashboard():
    if st.session_state.user:
        st.sidebar.title(f"Welcome, {st.session_state.user['full_name']}!")
    else:
        st.sidebar.title("Welcome!")
    
    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()
    
    menu = ["Search Buses", "My Bookings", "Profile"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Search Buses":
        search_buses()
    elif choice == "My Bookings":
        my_bookings()
    elif choice == "Profile":
        show_profile()

def search_buses():
    st.title("Search Buses")
    
    # Show available routes hint
    with st.expander("💡 Available Routes Hint"):
        st.write("""
        **Try these routes:**
        - Mumbai → Pune
        - Delhi → Jaipur  
        - Bangalore → Chennai
        - Hyderabad → Bangalore
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        source = st.text_input("From", placeholder="e.g., Mumbai")
    with col2:
        destination = st.text_input("To", placeholder="e.g., Pune")
    
    travel_date = st.date_input("Travel Date", datetime.now().date())
    seats = st.number_input("Number of Seats", min_value=1, max_value=10, value=1)
    
    # Show all buses button for debugging
    if st.button("Show All Available Buses"):
        show_all_buses(seats)
    
    if st.button("Search Buses"):
        if source and destination:
            search_and_display_buses(source, destination, seats)
        else:
            st.warning("Please enter source and destination.")

def search_and_display_buses(source, destination, seats):
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        # Get all buses first
        response = requests.get(f"{API_BASE_URL}/buses/", headers=headers)
        
        if response.status_code == 200:
            all_buses = response.json()
            
            # More flexible filtering
            filtered_buses = []
            for bus in all_buses:
                source_match = source.lower() in bus['source'].lower()
                destination_match = destination.lower() in bus['destination'].lower()
                
                if source_match and destination_match:
                    filtered_buses.append(bus)
            
            if filtered_buses:
                st.success(f"Found {len(filtered_buses)} bus(es) for {source} → {destination}")
                display_buses(filtered_buses, seats)
            else:
                st.warning(f"No direct buses found from {source} to {destination}")
                st.info("""
                **Available routes:**
                - Mumbai to Pune
                - Delhi to Jaipur
                - Bangalore to Chennai  
                - Hyderabad to Bangalore
                """)
                
                # Show all available buses for reference
                with st.expander("View All Available Buses"):
                    display_buses(all_buses, seats)
        else:
            st.error("Error fetching buses from server")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend server. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        st.error(f"Search error: {str(e)}")

def show_all_buses(seats):
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_BASE_URL}/buses/", headers=headers)
        
        if response.status_code == 200:
            all_buses = response.json()
            if all_buses:
                st.subheader("All Available Buses")
                display_buses(all_buses, seats)
            else:
                st.warning("No buses available in the system")
        else:
            st.error("Error fetching buses")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def display_buses(buses, seats):
    st.subheader("Available Buses")
    
    for bus in buses:
        # Convert string dates to datetime objects for display
        departure_time = datetime.fromisoformat(bus['departure_time'].replace('Z', '+00:00'))
        arrival_time = datetime.fromisoformat(bus['arrival_time'].replace('Z', '+00:00'))
        
        with st.expander(f"🚌 {bus['bus_number']} - {bus['route_name']}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**From:** {bus['source']}")
                st.write(f"**To:** {bus['destination']}")
            with col2:
                st.write(f"**Departure:** {departure_time.strftime('%Y-%m-%d %H:%M')}")
                st.write(f"**Arrival:** {arrival_time.strftime('%Y-%m-%d %H:%M')}")
            with col3:
                st.write(f"**Available Seats:** {bus['available_seats']}")
                st.write(f"**Base Price:** ₹{bus['base_price']} per seat")
            
            if bus['available_seats'] >= seats:
                if st.button(f"Book {seats} Seat(s)", key=f"book_{bus['id']}"):
                    book_bus(bus['id'], seats)
            else:
                st.warning("Not enough seats available")

def book_bus(bus_id, seats):
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.post(
            f"{API_BASE_URL}/bookings/",
            json={"bus_id": bus_id, "seats_booked": seats},
            headers=headers
        )
        
        if response.status_code == 200:
            booking = response.json()
            st.success(f"🎉 Booking confirmed! Reference: {booking['booking_reference']}")
            st.balloons()
            display_ticket(booking['id'])
        else:
            error_detail = response.json().get('detail', 'Unknown error')
            st.error(f"Booking failed: {error_detail}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend server. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        st.error(f"Booking error: {str(e)}")

def display_ticket(booking_id):
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(
            f"{API_BASE_URL}/bookings/{booking_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            ticket = response.json()
            
            st.subheader("🎫 Your E-Ticket")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Ticket Number:** {ticket['ticket_number']}")
                st.write(f"**Booking Reference:** {ticket['booking_reference']}")
                st.write(f"**Seats Booked:** {ticket['seats_booked']}")
                st.write(f"**Total Amount:** ₹{ticket['total_amount']}")
                st.write(f"**Status:** {ticket['booking_status']}")
                st.write(f"**Booked On:** {ticket['created_at']}")
            
            with col2:
                if ticket.get('qr_code_data'):
                    try:
                        # Display QR code
                        qr_image = base64.b64decode(ticket['qr_code_data'])
                        image = Image.open(io.BytesIO(qr_image))
                        st.image(image, caption="Scan for verification", width=200)
                    except Exception as e:
                        st.info("QR code generated successfully")
                else:
                    st.info("QR code will be generated for your ticket")
    except Exception as e:
        st.error(f"Error displaying ticket: {str(e)}")

def my_bookings():
    st.title("My Bookings")
    
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_BASE_URL}/bookings/my-bookings", headers=headers)
        
        if response.status_code == 200:
            bookings = response.json()
            if bookings:
                for booking in bookings:
                    with st.expander(f"Booking: {booking['booking_reference']} - ₹{booking['total_amount']}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Ticket Number:** {booking['ticket_number']}")
                            st.write(f"**Seats Booked:** {booking['seats_booked']}")
                            st.write(f"**Total Amount:** ₹{booking['total_amount']}")
                        with col2:
                            st.write(f"**Status:** {booking['booking_status']}")
                            st.write(f"**Booked on:** {booking['created_at']}")
                        
                        if st.button("View Ticket", key=f"view_{booking['id']}"):
                            display_ticket(booking['id'])
            else:
                st.info("No bookings found. Book your first trip!")
        else:
            st.error("Error fetching bookings.")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend server. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        st.error(f"Error: {str(e)}")

def show_profile():
    st.title("User Profile")
    
    # Get fresh user data
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(f"{API_BASE_URL}/users/me", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            st.write(f"**Name:** {user_data['full_name']}")
            st.write(f"**Email:** {user_data['email']}")
            st.write(f"**Phone:** {user_data.get('phone_number', 'Not provided')}")
            st.write(f"**Member since:** {user_data['created_at']}")
        else:
            st.error("Error loading profile data")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend server. Make sure the backend is running on http://localhost:8000")
    except Exception as e:
        st.error(f"Error loading profile: {str(e)}")

def main():
    st.set_page_config(
        page_title="Cloud Bus Pass System",
        page_icon="🚍",
        layout="wide"
    )
    
    init_session_state()
    
    if st.session_state.token is None:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            login()
        with tab2:
            register()
    else:
        dashboard()

if __name__ == "__main__":
    main()