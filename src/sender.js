import { ServiceBusClient } from "@azure/service-bus";
import dotenv from "dotenv";

dotenv.config();

const serviceBusClient = new ServiceBusClient(process.env.SERVICE_BUS_CONN_STR);

const sender = serviceBusClient.createSender("image-processesing-tasks");

const messages = [
  {
    body: "https://theimagestorage233.blob.core.windows.net/rawimages/image1.png",
  },
  {
    body: "https://theimagestorage233.blob.core.windows.net/rawimages/image2.jgp",
  },
  {
    body: "https://theimagestorage233.blob.core.windows.net/rawimages/image3.png",
  },
  {
    body: "https://theimagestorage233.blob.core.windows.net/rawimages/image4.jpg",
  },
  {
    body: "https://theimagestorage233.blob.core.windows.net/rawimages/image5.png",
  },
];

await sender.sendMessages(messages);
console.log("All messages sent");

/*
let batch = await sender.createMessageBatch();

for (let i = 0; i < messages.length; i++) {
  const message = messages[i];
  if (!batch.tryAddMessage(message)) {
    // Send the current batch as it is full and create a new one
    await sender.sendMessages(batch);
    batch = await sender.createMessageBatch();

    if (!batch.tryAddMessage(messages[i])) {
      throw new Error("Message too big to fit in a batch");
    }
  }
}
// Send the batch
await sender.sendMessages(batch);

*/
