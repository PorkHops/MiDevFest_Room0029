# backend/app.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory mock events (in real app: fetched via watsonx tools)
MOCK_EVENTS = [
    {
        "id": 1,
        "title": "Sunset Jazz at Riverside Park",
        "venue": "Riverside Park",
        "date": (datetime.now() + timedelta(hours=5)).isoformat(),
        "price": "Free",
        "image": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800",
        "url": "https://eventbrite.com/e/123",
        "summary": "Relaxing outdoor jazz with local artists"
    },
    {
        "id": 2,
        "title": "Vegan Night Market",
        "venue": "The Old Warehouse",
        "date": (datetime.now() + timedelta(days=1)).isoformat(),
        "price": "$5 entry",
        "image": "https://images.unsplash.com/photo-1606890737304-39519434f824?w=800",
        "url": "https://meetup.com/e/456",
        "summary": "30+ vegan vendors, live music, and cocktails"
    }
]

# Store user sessions (in prod: Redis + DB)
user_sessions = {}

@app.route('/api/events', methods=['GET'])
def get_events():
    user_id = request.args.get('user_id', 'anonymous')
    events = user_sessions.get(user_id, MOCK_EVENTS)
    return jsonify(events)

# Webhook to receive updates from watsonx Agent (you configure in watsonx console)
@app.route('/webhook/watsonx', methods=['POST'])
def watsonx_webhook():
    data = request.json
    user_id = data.get('user_id', 'anonymous')
    events = data.get('events', [])

    # Save and broadcast to frontend in real-time
    user_sessions[user_id] = events
    socketio.emit('events_update', {'user_id': user_id, 'events': events})
    
    return jsonify({"status": "received"}), 200

@socketio.on('connect')
def handle_connect():
    print('Client connected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)