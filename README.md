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

Procedure to connect to a private chat:

![image](https://github.com/Gpascual11/OnlineChatApplication_SD/assets/63343593/595e8a10-5228-41ee-a6f1-20b3d221747d)

Example of a private chat between to clients, user1 and user2:
![image](https://github.com/Gpascual11/OnlineChatApplication_SD/assets/63343593/d5448629-2d3b-40e9-9d90-3c105eae0040)


### Group Chats
The group chats are implemented using RabbitMQ, and they allow you to either connect or subscribe to a group chat.  Subscribing only allows you to receive messages, while
connecting allows you to send messages too, which is managed by the UI settings.  Moreover, once you select the type of chat you want, you can also select if you want it to be
persistent or transient.  The persistent version will allow new clients that connect later on to receive all the messages sent from the begining of the chat's existence.  This is
achieved creating a history queue that will store all messages sent to persistent chats, and every time a new client connects, it will check that queue and read the messages
that were sent to the chat before its arrival.

Example of a group chat with three users:
![image](https://github.com/Gpascual11/OnlineChatApplication_SD/assets/63343593/bce7da47-b1c8-4877-be47-8e82cb5c90b3)



### Discovery Service
In order to obtain the connection parameters of the connected clients, we have implemented the discovery service.  It provides two options: Redis and RabbitMQ.  The firs one gets
the clients information from the shared memory in the Redis server, while the second one uses the RabbitMQ broker to send a discovery message to all clients, who reply with a 
direct message to the requesting client with their connection parameters.

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
