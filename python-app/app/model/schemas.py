from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict


class Location(BaseModel):
    city: Optional[str]
    latitude: float
    longitude: float


class WeatherPayload(BaseModel):
    source: str
    location: Location
    observed_at: datetime
    temperature_c: Optional[float]
    humidity_percent: Optional[float]
    wind_speed_m_s: Optional[float]
    wind_direction_deg: Optional[float]
    cloud_cover_percent: Optional[float]
    precipitation_probability: Optional[float]
    raw: Optional[Dict] = Field(default_factory=dict)
