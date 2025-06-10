import json
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
import os
from dotenv import load_dotenv

load_dotenv()
SERVICE_BUS_CONNECTION_STRING = os.getenv("SERVICE_BUS_CONNECTION_STRING")
TOPIC_NAME = os.getenv("TOPIC_NAME")
SUBSCRIPTION_NAME = os.getenv("SUBSCRIPTION_NAME")

async def send_notification_message(message: dict):
    async with ServiceBusClient.from_connection_string(SERVICE_BUS_CONNECTION_STRING) as client:
        sender = client.get_topic_sender(topic_name=TOPIC_NAME)
        async with sender:
            msg = json.dumps(message)
            await sender.send_messages(ServiceBusMessage(msg))
