import { format, isToday, isTomorrow, addDays } from "date-fns";
import EventCard from "./EventCard";
import type { Event } from "../types";

export default function EventTimeline({ events }: { events: Event[] }) {
  const groupByDay = () => {
    const groups: Record<string, Event[]> = {};
    events.forEach((event) => {
      const date = new Date(event.date);
      let key = "";
      if (isToday(date)) key = "Today";
      else if (isTomorrow(date)) key = "Tomorrow";
      else if (date < addDays(new Date(), 7)) key = format(date, "EEEE");
      else key = "Upcoming";

      if (!groups[key]) groups[key] = [];
      groups[key].push(event);
    });
    return groups;
  };

  const groups = groupByDay();

  return (
    <div>
      {Object.keys(groups).length === 0 ? (
        <div className="empty-state">
          <p className="empty-title">No events yet...</p>
          <p>Chat with me to discover events you'll love!</p>
        </div>
      ) : (
        Object.keys(groups).map((day) => (
          <section key={day} className="timeline-section">
            <h2 className="timeline-header">{day}</h2>
            <div className="event-grid">
              {groups[day].map((event) => (
                <EventCard key={event.id} event={event} />
              ))}
            </div>
          </section>
        ))
      )}
    </div>
  );
}
