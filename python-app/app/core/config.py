import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    weather_provider: str = os.getenv("WEATHER_PROVIDER", "open-meteo")
    latitude: float = float(os.getenv("LATITUDE", "0"))
    longitude: float = float(os.getenv("LONGITUDE", "0"))
    interval_seconds: int = int(os.getenv("WEATHER_INTERVAL_SECONDS", "3600"))

    rabbitmq_url: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    rabbitmq_exchange: str = os.getenv("RABBITMQ_EXCHANGE", "weather_exchange")
    rabbitmq_queue: str = os.getenv("RABBITMQ_QUEUE", "weather_queue")
    rabbitmq_routing_key: str = os.getenv("RABBITMQ_ROUTING_KEY", "weather.logs")

    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
