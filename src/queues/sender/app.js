import express from "express";
import { ServiceBusClient } from "@azure/service-bus";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(express.json());

const connectionString = process.env.SERVICE_BUS_CONN_STR;
const queueName = "image-processesing-tasks";

async function processMessageSending(message) {
  const sbClient = new ServiceBusClient(connectionString);
  const sender = sbClient.createSender(queueName);

  try {
    const msg = { body: message };
    await sender.sendMessages(msg);
    console.log(`Message sent: ${message}`);
  } catch (err) {
    console.error("Error sending message:", err);
  } finally {
    await sbClient.close();
  }
}

app.post("/send", async (req, res) => {
  const message = req.body.message;
  if (!message) {
    return res.status(400).send("Missing message in request body");
  }
  await processMessageSending(message);
  res.send("Message sent successfully");
});

const port = process.env.PORT || 4000;
app.listen(port, () => console.log(`Sender app listening on port ${port}`));
