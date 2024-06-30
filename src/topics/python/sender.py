import asyncio
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from dotenv import load_dotenv
import os

load_dotenv()

NAMESPACE_CONNECTION_STR = os.getenv("SERVICE_BUS_CONN_STR_WITH_TOPIC")
TOPIC_NAME = "mytopic"

async def send_single_message(sender):
    # Create a Service Bus message
    message = ServiceBusMessage("Single Message")
    # send the message to the topic
    await sender.send_messages(message)
    print("Sent a single message")

async def send_a_list_of_messages(sender):
    # Create a list of messages
    messages = [ServiceBusMessage("Message in list") for _ in range(5)]
    # send the list of messages to the topic
    await sender.send_messages(messages)
    print("Sent a list of 5 messages")

async def send_batch_message(sender):
    # Create a batch of messages
    async with sender:
        batch_message = await sender.create_message_batch()
        for _ in range(10):
            try:
                # Add a message to the batch
                batch_message.add_message(ServiceBusMessage("Message inside a ServiceBusMessageBatch"))
            except ValueError:
                # ServiceBusMessageBatch object reaches max_size.
                # New ServiceBusMessageBatch object can be created here to send more data.
                break
        # Send the batch of messages to the topic
        await sender.send_messages(batch_message)
    print("Sent a batch of 10 messages")


async def run():
    # create a Service Bus client using the connection string
    async with ServiceBusClient.from_connection_string(
        conn_str=NAMESPACE_CONNECTION_STR,
        logging_enable=True) as servicebus_client:
        # Get a Topic Sender object to send messages to the topic
        sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
        async with sender:
            # Send one message
            await send_single_message(sender)
            # Send a list of messages
            await send_a_list_of_messages(sender)
            # Send a batch of messages
            await send_batch_message(sender)

asyncio.run(run())
print("Done sending messages")
print("-----------------------")