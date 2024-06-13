import { ServiceBusClient } from "@azure/service-bus";
import dotenv from "dotenv";
dotenv.config();

const connectionString = process.env.SERVICE_BUS_CONN_STR;
const queueName = "image-processesing-tasks";

async function receiveMessages() {
  const sbClient = new ServiceBusClient(connectionString);
  const receiver = sbClient.createReceiver(queueName);

  try {
    while (true) {
      // Loop to continuously receive messages
      const messages = await receiver.receiveMessages(10, 10000); // Receive up to 10 messages with 10 second timeout
      if (messages.length === 0) {
        console.log("No messages received. Waiting...");
        await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait 1 second before checking again
      } else {
        for (const message of messages) {
          console.log(`Received message: ${message.body}`);
          // Process the message content here
          // You can also acknowledge receiving the message to remove it from the queue
          await receiver.completeMessage(message);
        }
      }
    }
  } catch (err) {
    console.error("Error receiving message:", err);
  } finally {
    await sbClient.close();
  }
}

receiveMessages();
