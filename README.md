# Application Chat Documentation
This project has been developed for the Distributed Systems course (URV, 2024) and implements a chat system using different approaches, from gRPC for private chats,
to Redis for shared memory and RabbitMQ for the group chats implementation and discovery features.

## Project Description
The aim of this project is to demonstrate a basic implementation of a distributed architecture and how different technologies work.
Therefore, the application works launching different clients on different terminals in the same machine
instead of using a real distributed system.  Each client has, apart from its basic connection parameters (IP address and port), a client ID, that is generated randomly
upon startup.  This unique ID is used to identify the client, and all connections are depending on it.  This means that, for instance, when connecting to a private chat,
you will be asked to provide the client ID of the client you want to start the chat with. 

### Private Chats
Private chats are directly implemented using gRPC, and, as stated earlier, they use the client ID to identify each client and the connection.  The chat itself is shown in
a separate UI that presents the messages sent by the user on the right, and the ones received on the left.  Moreover, in case one of the clients disconects, a disconnect
message is shown in the middle of the UI before closing it, as it serves no pourpose to have the UI open once one of the clients has ended the chat.

![image](https://github.com/Gpascual11/OnlineChatApplication_SD/assets/63343593/694a5d11-9820-4a00-8a3c-951a1f290412)



The group chats and the insult server are implemented using two different architectures of the provided by RabbitMQ, and they allow you to either connect or subscribe to 
a group chat, that can be persistent or transient, and connect to an "insult service" that allows you to send messages to one random recipient from the clients connected
to that service.  Regarding the discovery function, it can be performed through Redis, using the shared memory it provides, or asking the other clients directly through
the RabbitMQ broker.  In both cases, it provides the connection parameters of all the connected clients.

## Requirements
The project is implemented using the following:
- Python v3.11.8 with grpcio v1.62.1
- Conda v24.1.2
- Docker v26.1.2, with the Redis and RabbitMQ containers.

## How To Use
In order to setup the gRPC, Redis and RabbitMQ servers, exectute the ```start-server.sh``` script.

Then, execute as many clients as needed running the ```start-client.sh``` script.

## Evaluation Questions
Q1:  Private chats are not persistent, and would require something like a log system on a file to be able to keep track of all the messages sent,
  which is not implemented in this version of the system.

Q2: RabbitMQ systems can be considered stateful, as they keep track of the state of messages, queues, and connections among other things.

Q3: Group chats are implemented using a publisher/subscriber pattern.  Transient chats only require the basic queues and an exchange, while persistent ones require an extra
  queue to store all the messages sent to the chats.
