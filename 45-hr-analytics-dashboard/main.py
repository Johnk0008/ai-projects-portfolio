# main.py
from app.dashboard import app

if __name__ == '__main__':
    print("Starting HR Analytics Dashboard...")
    print("Access the dashboard at: http://localhost:8050")
    app.run_server(debug=True, port=8050)