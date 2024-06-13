import { ServiceBusClient } from "@azure/service-bus";
import dotenv from "dotenv";

dotenv.config();

const serviceBusClient = new ServiceBusClient(process.env.SERVICE_BUS_CONN_STR);
const receiver = serviceBusClient.createReceiver("image-processesing-tasks");

const myMessages = await receiver.receiveMessages(3);
console.log(myMessages);
console.log("new batch received");
