import asyncio
import aio_pika

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
AMQP_ADDRESS = os.environ.get("AMQP_ADDRESS")
EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME")
BINDING_KEYS = [os.environ.get("BINDING_KEY_A"), os.environ.get("BINDING_KEY_B")]
QUEUE_NAME = "consumer_a"


async def receive_amqp_messages():
    # connect to server

    connection: aio_pika.robust_connection.RobustConnection = await aio_pika.connect_robust(AMQP_ADDRESS)
    async with connection:
        channel: aio_pika.channel.Channel = await connection.channel()

        # declaring exchange
        exchange: aio_pika.exchange.Exchange = await channel.declare_exchange(
            EXCHANGE_NAME,
            aio_pika.ExchangeType.TOPIC,
            durable=True,
        )

        # declaring queue
        queue: aio_pika.queue.Queue = await channel.declare_queue(
            QUEUE_NAME,
            durable=True,
            arguments={"x-queue-type": "quorum", "x-single-active-consumer": True},
        )

        # binding queue to exchange
        for topic in BINDING_KEYS:
            await queue.bind(exchange, routing_key=topic)

        # listen
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = message.body.decode("utf-8")
                    print(f"Message body is:{payload}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(receive_amqp_messages())
