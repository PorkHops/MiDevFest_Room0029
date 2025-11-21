# Event Lite

**Your personal local event curator — powered by IBM watsonx AI**

Event Lite asks you what you’re in the mood for, then instantly shows you the best local events happening today, tomorrow, and this week — no endless scrolling required.

Live demo: Open the app → grant location → tap the purple chat bubble → tell the AI what you love (e.g. “I’m into techno, vegan food, and free events under $30”) → watch the timeline update in real time.

## Features

- Real-time personalized event discovery via IBM watsonx agent
- Beautiful daily timeline (Today / Tomorrow / This Weekend)
- One-tap “Interested” + open-in-new-tab
- Works offline (PWA — installable on phone/desktop)
- Zero Tailwind bloat — pure vanilla CSS + TypeScript
- Real-time sync via Flask + Socket.IO

## Tech Stack

- **Frontend**: React 18 + Vite + TypeScript + UUID + vanilla CSS
- **Backend**: Python Flask + Flask-SocketIO + CORS
- **AI Brain**: IBM watsonx Orchestrate Agent (embedded chat)
- **Realtime**: Socket.IO (full-duplex)

## Quick Start (2 terminals)

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/event-lite.git
cd event-lite

cd backend

# Create and activate virtual env
python -m venv venv
# Windows (Git Bash / CMD):
venv\Scripts\activate
# macOS / Linux:
# source venv/bin/activate

# Install dependencies
pip install Flask flask-socketio flask-cors python-socketio eventlet

# Run
python app.py

cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```
