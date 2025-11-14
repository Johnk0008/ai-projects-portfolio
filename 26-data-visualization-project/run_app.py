#!/usr/bin/env python3
"""
Main application runner for Data Visualization Project
"""

import argparse
from src.dashboard import InteractiveDashboard, create_streamlit_app

def main():
    parser = argparse.ArgumentParser(description="Data Visualization Dashboard")
    parser.add_argument('--app', type=str, choices=['dash', 'streamlit'], 
                       default='dash', help='Choose which app to run')
    
    args = parser.parse_args()
    
    if args.app == 'dash':
        print("Starting Dash application...")
        dashboard = InteractiveDashboard()
        dashboard.run(debug=True)
    else:
        print("To run Streamlit app, execute: streamlit run src/dashboard.py")
        # create_streamlit_app()  # Uncomment for Streamlit

if __name__ == "__main__":
    main()