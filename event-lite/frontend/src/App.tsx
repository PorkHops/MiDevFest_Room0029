import { useState, useEffect, useMemo } from "react";
import { io, Socket } from "socket.io-client";
import { v4 as uuidv4 } from "uuid";
import EventTimeline from "./components/EventTimeline";
import LocationSelector from "./components/LocationSelector";
import "./index.css"; // Import vanilla CSS

type Location = { lat: number; lng: number } | null;

interface Event {
  id: string | number;
  title: string;
  venue: string;
  date: string;
  price: string;
  image: string;
  url: string;
  summary: string;
}

const socket: Socket = io("http://localhost:5001");

function App() {
  const [events, setEvents] = useState<Event[]>([]);
  const [location, setLocation] = useState<Location>(null);

  // Pure, stable userId using useMemo + UUID
  const userId = useMemo(() => {
    return "user_" + uuidv4().slice(0, 8);
  }, []);

  useEffect(() => {
    // Geolocation
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) =>
          setLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
        () => console.log("Location permission denied")
      );
    }

    // Initial events
    fetch(`http://localhost:5001/api/events?user_id=${userId}`)
      .then((r) => r.json())
      .then((data) => setEvents(data));

    // Real-time updates from watsonx → backend → socket
    socket.on("events_update", (data: { user_id: string; events: Event[] }) => {
      if (data.user_id === userId) {
        setEvents(data.events);
      }
    });

    return () => {
      socket.off("events_update");
    };
  }, [userId]);

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <h1>Event Lite</h1>
          <LocationSelector location={location} setLocation={setLocation} />
        </div>
      </header>

      <main className="main">
        <EventTimeline events={events} />
      </main>

      {/* Floating watsonx chat toggle */}
      <div>
        <button
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          onClick={() => (window as any).wxoChat?.toggle?.()}
          className="chat-toggle"
        >
          <svg
            className="chat-icon"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
        </button>
      </div>
    </div>
  );
}

export default App;
