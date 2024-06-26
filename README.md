# Application Chat Documentation
This project has been developed for the Distributed Systems course (URV, 2024) and implements a chat system using different approaches.

## Project Description
The aim of this project is to demonstrate a basic implementation of a distributed architecture and how different technologies work.
Therefore, the application works launching different clients on different terminals in the same machine
instead of using a real distributed system.  Each client has, apart from its basic connection parameters (IP address and port), a client ID, that is generated randomly
upon startup.  This unique ID is used to identify the client, and all connections are depending on it.  This means that, for instance, when connecting to a private chat,
you will be asked to provide the client ID of the client you want to start the chat with. 

Group chat communication is implemented via RabbitMQ and uses a queue system to send the messages to the clients connected to a specific chat.  It also implements persistency with an auxiliary queue.
The discovery functionality allows users to get the connection parameters of the rest of the users connected, and it can be performed via Redis, using the NameServer
or via RabbitMQ, sending a discovery message.  Finally, the insult server is implemented via RabbitMQ using a message queue instead of a publisher/subscriber pattern as done in
the group chats, and it allows you to send insults to a queue that will distribute them to one of the connected clients.  For more information about the implementation of each feature,
check the explanations below.


### Private Chats
Private chats are directly implemented using gRPC, and, as stated earlier, they use the client ID to identify each client and the connection.  The chat itself is shown in
a separate UI that presents the messages sent by the user on the right, and the ones received on the left.  Moreover, in case one of the clients disconnects, a disconnect
message is shown in the middle of the UI before closing it, as it serves no purpose to have the UI open once one of the clients has ended the chat.

Procedure to connect to a private chat:

![image](https://github.com/Gpascual11/OnlineChatApplication_SD/assets/63343593/595e8a10-5228-41ee-a6f1-20b3d221747d)

Example of a private chat between to clients, user1 and user2:
![image](https://github.com/Gpascual11/OnlineChatApplication_SD/assets/63343593/d5448629-2d3b-40e9-9d90-3c105eae0040)


### Group Chats
The group chats are implemented using RabbitMQ, and they allow you to either connect or subscribe to a group chat.  Subscribing only allows you to receive messages, while
connecting allows you to send messages too, which is managed by the UI settings.  Moreover, once you select the type of chat you want, you can also select if you want it to be
persistent or transient.  The persistent version will allow new clients that connect later to receive all the messages sent from the beginning of the chat's existence.  This is
achieved creating a history queue that will store all messages sent to persistent chats, and every time a new client connects, it will check that queue and read the messages
that were sent to the chat before its arrival.

Example of a group chat with three users:
![image](https://github.com/Gpascual11/OnlineChatApplication_SD/assets/63343593/a47eb0dc-6b08-4a75-b0fd-472b406da906)



### Discovery Service
In order to obtain the connection parameters of the connected clients, we have implemented the discovery service.  It provides two options: Redis and RabbitMQ.  The firs one gets
the clients information from the shared memory in the Redis server, while the second one uses the RabbitMQ broker to send a discovery message to all clients, who reply with a 
direct message to the requesting client with their connection parameters.

Example of discovery with Redis:
![image](https://github.com/Gpascual11/OnlineChatApplication_SD/assets/63343593/9eb34e03-f867-4eb1-85c7-08d868e70722)

Example of discovery using RabbitMQ:
![image](https://github.com/Gpascual11/OnlineChatApplication_SD/assets/63343593/9fa2bc0a-b8b5-44d6-b575-a6831a6389b8)



### Insult Service
The insult service is implemented using a message queue pattern through RabbitMQ.  When a client connects to it, the UI is launched and gives the option to send an insult to the queue.
Each insult queued is sent to only one of the connected clients. Example:

![image](https://github.com/Gpascual11/OnlineChatApplication_SD/assets/63343593/514e9bae-db78-4e46-97de-dd071383e2a8)


## Requirements
The project is implemented using the following:
- Python v3.11.8 with grpcio v1.62.1
- Conda v24.1.2
- Docker v26.1.2, with the Redis and RabbitMQ containers.

## How To Use
In order to setup the gRPC, Redis and RabbitMQ servers, execute the ```start-server.sh``` script.

Then, execute as many clients as needed running the ```start-client.sh``` script.

## Evaluation Questions
Q1:  Private chats are not persistent and would require something like a log system on a file to be able to keep track of all the messages sent,
  which is not implemented in this version of the system.

Q2: RabbitMQ systems can be considered stateful, as they keep track of the state of messages, queues, and connections among other things.

Q3: Group chats are implemented using a publisher/subscriber pattern.  Transient chats only require the basic queues and an exchange, while persistent ones require an extra
  queue to store all the messages sent to the chats.
