### Application Chat Documentation
This project has been developed for the Distributed Systems course (URV, 2024) and implements a chat system using different approaches, from gRPC for private chats,
to Redis for shared memory and RabbitMQ for the group chats implementation and discovery features.

## Requirements
The project is implemented using the following:
- Python v3.11.8 with grpcio v1.62.1
- Conda v24.1.2
- Docker v26.1.2, with the Redis and RabbitMQ containers.

## How To Use
In order to setup the gRPC, Redis and RabbitMQ servers, exectute the ```start-server.sh``` script.

Then, execute as many clients as needed running the ```start-client.sh``` script.
