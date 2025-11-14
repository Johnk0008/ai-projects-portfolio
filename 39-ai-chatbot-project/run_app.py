import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from web_app.app import app, socketio

if __name__ == '__main__':
    print("🚀 Starting AI Chatbot Web Application...")
    print("📧 Open http://localhost:5000 in your browser")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)