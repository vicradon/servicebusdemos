import os
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage

load_dotenv()
service_bus_conn_str = os.getenv("SERVICE_BUS_CONN_STR")
queue_name = "image-processesing-tasks";


while True:
    with ServiceBusClient.from_connection_string(service_bus_conn_str) as client:
        with client.get_queue_receiver(queue_name, max_wait_time=10) as receiver:
            for msg in receiver: 
                print(str(msg))
                receiver.complete_message(msg)

