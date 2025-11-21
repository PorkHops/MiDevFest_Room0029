import { format } from "date-fns";
import { Heart, ExternalLink } from "lucide-react";
import type { Event } from "../types";

export default function EventCard({ event }: { event: Event }) {
  return (
    <div className="event-card">
      <img src={event.image} alt={event.title} className="event-image" />
      <div className="event-content">
        <h3 className="event-title">{event.title}</h3>
        <p className="event-venue">{event.venue}</p>
        <p className="event-date">
          {format(new Date(event.date), "h:mm a · EEE, MMM d")}
        </p>
        <p className="event-price">{event.price}</p>
        <p className="event-summary">{event.summary}</p>

        <div className="event-actions">
          <button className="interested-btn">
            <Heart className="inline w-5 h-5 mr-2" /> Interested
          </button>
          <a
            href={event.url}
            target="_blank"
            rel="noopener noreferrer"
            className="external-link"
          >
            <ExternalLink className="w-5 h-5" />
          </a>
        </div>
      </div>
    </div>
  );
}
