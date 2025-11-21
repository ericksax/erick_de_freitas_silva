import logging
import httpx
from typing import Any


from ..core.config import settings


log = logging.getLogger("weather_client")


class WeatherClient:
    def __init__(self, settings):
        self.settings = settings

    async def fetch(self) -> Any:
        provider = self.settings.weather_provider.lower()
        if provider == "open-meteo":
            return await self._fetch_open_meteo()
        elif provider == "openweather":
            return await self._fetch_openweather()
        else:
            raise ValueError("Unknown provider")

    async def _fetch_open_meteo(self) -> Any:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.settings.latitude,
            "longitude": self.settings.longitude,
            "current_weather": "true",
            "hourly": "relativehumidity_2m,precipitation_probability,cloudcover",
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            r = await client.get(url, params=params)
            r.raise_for_status()
            log.debug("Open-Meteo response: %s", r.text)
            return r.json()

    async def _fetch_openweather(self) -> Any:
        # Placeholder: OpenWeather requires API key; implement if using it
        raise NotImplementedError(
            "OpenWeather provider is not implemented in this template"
        )
