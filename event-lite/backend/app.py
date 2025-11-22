# backend/app.py
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests
import json
from datetime import datetime, timedelta
from events import get_events as get_events_list

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

def get_location_by_ip():
    try:
        response = requests.get('https://ipapi.co/json/')
        data = response.json()
        
        return {
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country_name'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timezone': data.get('timezone')
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

location = get_location_by_ip()

# get some fake events
with open('DBEvents.json', 'r') as f:
    MOCK_EVENTS = json.load(f)

# TESTING PURPOSE
# MOCK_EVENTS = MOCK_EVENTS[:5]

# Fetch real events using events.py
# MOCK_EVENTS.extend(get_events_list(location))

# Sort events by date
MOCK_EVENTS.sort(key=lambda x: x['date'])

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