import json
import time
import asyncio
import aio_pika

import os
from random import randint
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
AMQP_ADDRESS = os.environ.get("AMQP_ADDRESS")
EXCHANGE_NAME = os.environ.get("EXCHANGE_NAME")
BINDING_KEYS = [os.environ.get("BINDING_KEY_A"), os.environ.get("BINDING_KEY_B")]


async def emit(channel: aio_pika.channel.Channel, route: str, data: dict):
    # declaring exchange
    exchange: aio_pika.exchange.Exchange = await channel.declare_exchange(
        EXCHANGE_NAME,
        aio_pika.ExchangeType.TOPIC,
        durable=True,
    )
    # Sending the message
    message_body = json.dumps(data)
    message = aio_pika.Message(message_body.encode())
    await exchange.publish(message, routing_key=route)


async def emit_amqp_messages(channel: aio_pika.channel.Channel):
    for topic in BINDING_KEYS:
        for num in range(randint(1, 5)):
            await emit(channel, topic, f"{num+1}# payload sent with topic[{topic}]")


async def retry_if_connection_fails(retries: int, delay: int):
    # A custom retry loop
    for i in range(retries):
        try:
            # connect to server
            connection: aio_pika.robust_connection.RobustConnection = await aio_pika.connect_robust(AMQP_ADDRESS)
            channel: aio_pika.channel.Channel = await connection.channel()

            # send a ramdom number of predefined messages to given conenction
            await emit_amqp_messages(channel)

            # close connection
            await connection.close()

            # if everything went down without exceptions, exit
            return

        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
                print(e)
                continue
            else:
                print("failed to emit {data} \n amqp producer out of connection retries")
                raise


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(retry_if_connection_fails(20, 0.5))
