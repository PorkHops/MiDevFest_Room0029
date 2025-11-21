import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EventFetcher:
    def __init__(self):
        # API key from environment variable
        self.eventbrite_token = os.environ.get("EVENTBRITE_TOKEN")

    def get_user_location(self, ip_address: Optional[str] = None) -> Dict[str, str]:
        try:
            # Use ipapi.co for IP geolocation (free tier available)
            if ip_address:
                response = requests.get(
                    f"https://ipapi.co/{ip_address}/json/", timeout=5
                )
            else:
                response = requests.get("https://ipapi.co/json/", timeout=5)

            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data.get("city", "Unknown"),
                    "country": data.get("country_name", "Unknown"),
                    "lat": data.get("latitude"),
                    "lon": data.get("longitude"),
                    "region": data.get("region", ""),
                }
        except Exception as e:
            print(f"Error getting location: {e}")

        # Fallback to default location
        return {
            "city": "San Francisco",
            "country": "United States",
            "lat": 37.7749,
            "lon": -122.4194,
            "region": "California",
        }

    def get_date_range(self) -> tuple:
        """Get date range for next 7 days."""
        today = datetime.now()
        end_date = today + timedelta(days=7)
        return today, end_date

    def fetch_eventbrite_events(
        self, location: Dict, start_date: datetime, end_date: datetime
    ) -> List[Dict]:
        if not self.eventbrite_token:
            print("Eventbrite token not configured.")
            return []

        events = []
        try:
            url = "https://www.eventbriteapi.com/v3/events/search/"
            headers = {"Authorization": f"Bearer {self.eventbrite_token}"}
            params = {
                "location.address": location["city"],
                "start_date.range_start": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "start_date.range_end": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "expand": "venue,ticket_availability",
                "page_size": 20,
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()

                for idx, event in enumerate(data.get("events", [])):
                    events.append(self._format_eventbrite_event(event, idx))
        except Exception as e:
            print(f"Error fetching Eventbrite events: {e}")

        return events

    def _format_eventbrite_event(self, event: Dict, idx: int) -> Dict:
        """Format Eventbrite event to standardized format."""
        # Get venue
        venue_name = "Online Event"
        if event.get("venue"):
            venue_name = event["venue"].get("name", "TBA")

        # Get price
        is_free = event.get("is_free", False)
        price = "Free" if is_free else "See website"

        # Get image
        logo = event.get("logo", {})
        image_url = logo.get("original", {}).get(
            "url", "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=800"
        )

        return {
            "id": idx + 1,
            "title": event.get("name", {}).get("text", "Untitled Event"),
            "venue": venue_name,
            "date": event.get("start", {}).get("local", ""),
            "price": price,
            "image": image_url,
            "url": event.get("url", ""),
            "summary": event.get(
                "summary", event.get("description", {}).get("text", "")
            )[:100],
        }

    def get_events_for_user(self, location: Optional[Dict[str, str]] = None) -> List[Dict]:
        # Get user location
        print(f"Fetching events for {location['city']}, {location['country']}")

        # Get date range (next 7 days)
        start_date, end_date = self.get_date_range()

        # Fetch from Eventbrite
        all_events = []

        if self.eventbrite_token:
            all_events = self.fetch_eventbrite_events(location, start_date, end_date)
            print(f"Fetched {len(all_events)} events from Eventbrite")
        else:
            print("No Eventbrite API token configured, using mock data")
            # all_events = self._get_mock_events(start_date, end_date)

        # Sort by date
        all_events.sort(key=lambda x: x.get("date", ""))

        return all_events

    def _get_mock_events(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        import json
        try:
            with open("DBEvents.json", "r") as f:
                mock_events = json.load(f)

            # Filter events within date range
            filtered_events = []
            for event in mock_events:
                event_date = datetime.fromisoformat(
                    event["date"].replace("Z", "+00:00")
                )
                if start_date <= event_date <= end_date:
                    filtered_events.append(event)

            return filtered_events
        except Exception as e:
            print(f"Error loading mock events: {e}")
            return []


# Convenience function for easy import
def get_events(location: Dict[str, str] = None) -> List[Dict]:
    fetcher = EventFetcher()
    return fetcher.get_events_for_user(location)