from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from chatbot.chatbot_core import ChatbotCore

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize chatbot
chatbot = ChatbotCore('data/intents.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    try:
        user_message = request.json.get('message', '')
        
        if not user_message.strip():
            return jsonify({'error': 'Empty message'}), 400
        
        response = chatbot.get_response(user_message)
        
        return jsonify({
            'user_message': user_message,
            'bot_response': response['response'],
            'confidence': response['confidence'],
            'method': response['method'],
            'intent': response['intent']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('send_message')
def handle_message(data):
    try:
        user_message = data.get('message', '')
        
        if user_message.strip():
            response = chatbot.get_response(user_message)
            
            emit('receive_message', {
                'user_message': user_message,
                'bot_response': response['response'],
                'confidence': response['confidence'],
                'method': response['method'],
                'intent': response['intent'],
                'timestamp': data.get('timestamp')
            })
            
    except Exception as e:
        emit('error', {'error': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)