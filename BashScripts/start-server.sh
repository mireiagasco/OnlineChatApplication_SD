#!/bin/bash

# Function to start the server
start_server() {
    echo "Starting the server..."
    docker run -d --rm --name REDIS -p 6379:6379 redis:alpine
    docker run -d --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
    echo "Server started."
    sleep 10
    echo "Opening RabbitMQ management interface in your default browser..."
    xdg-open "http://localhost:15672/#/"
    sleep 5
}

# Function to stop the server
stop_server() {
    echo "Stopping the server..."
    docker stop rabbitmq
    docker stop REDIS
    echo "Server stopped."
}

# Main loop
while true; do
    echo "Select an option:"
    echo "1. Start the server"
    echo "2. Stop the server"
    read option

    case $option in
        1)
            start_server
            ;;
        2)
            stop_server
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
done
