import json
import logging
import asyncio
from aio_pika import connect_robust, Message, ExchangeType
from tenacity import retry, stop_after_attempt, wait_exponential


log = logging.getLogger("publisher")


class Publisher:
    def __init__(self, settings):
        self.settings = settings
        self._connection = None
        self._channel = None
        self._exchange = None

    @retry(
        stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def connect(self):
        log.info("Connecting to RabbitMQ: %s", self.settings.rabbitmq_url)
        self._connection = await connect_robust(self.settings.rabbitmq_url)
        self._channel = await self._connection.channel()
        self._exchange = await self._channel.declare_exchange(
            self.settings.rabbitmq_exchange, ExchangeType.DIRECT, durable=True
        )
        # declare queue and bind
        queue = await self._channel.declare_queue(
            self.settings.rabbitmq_queue, durable=True
        )
        await queue.bind(self._exchange, routing_key=self.settings.rabbitmq_routing_key)
        log.info("Connected and queue declared")

    async def publish(self, payload: dict):
        if not self._exchange:
            await self.connect()
        body = json.dumps(payload, default=str).encode()
        message = Message(body, delivery_mode=2)
        await self._exchange.publish(
            message, routing_key=self.settings.rabbitmq_routing_key
        )
        log.info("Published message observed_at=%s", payload.get("observed_at"))

    async def close(self):
        try:
            if self._connection:
                await self._connection.close()
        except Exception:
            log.exception("Error closing RabbitMQ connection")
