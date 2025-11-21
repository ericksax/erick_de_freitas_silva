from datetime import datetime, timezone
from typing import Any, Dict


from ..core.config import settings


class Normalizer:
    def __init__(self, settings):
        self.settings = settings

    def normalize(self, raw: Any) -> Dict:
        # Use a normalized structure that matches worker expectations
        provider = self.settings.weather_provider.lower()
        now = datetime.now(timezone.utc).isoformat()
        if provider == "open-meteo":
            cur = raw.get("current_weather", {})
            payload = {
                "source": "open-meteo",
                "location": {
                    "city": None,
                    "latitude": self.settings.latitude,
                    "longitude": self.settings.longitude,
                },
                "observed_at": cur.get("time", now),
                "temperature_c": cur.get("temperature"),
                "humidity_percent": None,
                "wind_speed_m_s": cur.get("windspeed"),
                "wind_direction_deg": cur.get("winddirection"),
                "cloud_cover_percent": None,
                "precipitation_probability": None,
                "raw": raw,
            }
            return payload
        else:
            raise NotImplementedError

    # helper used by routes.trigger (optional quick trigger)


async def trigger_once_normalize():
    # Kept for compatibility if needed; real trigger uses scheduler.trigger_once
    return {}
