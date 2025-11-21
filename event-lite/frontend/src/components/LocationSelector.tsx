import { MapPin } from "lucide-react";

type Location = { lat: number; lng: number } | null;

interface Props {
  location: Location;
  setLocation: (loc: Location) => void;
}

export default function LocationSelector({ location }: Props) {
  return (
    <div className="location-selector">
      <MapPin className="location-icon" />
      <span>
        {location
          ? `Lat ${location.lat.toFixed(2)}, Lng ${location.lng.toFixed(2)}`
          : "Location detecting..."}
      </span>
    </div>
  );
}
