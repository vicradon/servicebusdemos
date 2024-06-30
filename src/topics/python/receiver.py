import asyncio
import signal
from azure.servicebus.aio import ServiceBusClient
from dotenv import load_dotenv
import os

load_dotenv()

NAMESPACE_CONNECTION_STR = os.getenv("SERVICE_BUS_CONN_STR_WITH_TOPIC")
SUBSCRIPTION_NAME = "S1"
TOPIC_NAME = "mytopic"

stop_event = asyncio.Event()

def handle_sigterm():
    stop_event.set()

async def run():
    # create a Service Bus client using the connection string
    async with ServiceBusClient.from_connection_string(
        conn_str=NAMESPACE_CONNECTION_STR,
        logging_enable=True) as servicebus_client:

        # get the Subscription Receiver object for the subscription
        receiver = servicebus_client.get_subscription_receiver(
            topic_name=TOPIC_NAME, 
            subscription_name=SUBSCRIPTION_NAME, 
            max_wait_time=5)

        async with receiver:
            while not stop_event.is_set():
                received_msgs = await receiver.receive_messages(max_wait_time=5, max_message_count=20)
                for msg in received_msgs:
                    print("Received: " + str(msg))
                    # complete the message so that the message is removed from the subscription
                    await receiver.complete_message(msg)

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.add_signal_handler(signal.SIGTERM, handle_sigterm)
    loop.add_signal_handler(signal.SIGINT, handle_sigterm)

    try:
        loop.run_until_complete(run())
    finally:
        loop.close()

if __name__ == "__main__":
    main()


