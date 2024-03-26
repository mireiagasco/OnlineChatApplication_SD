#!/bin/bash

# Function to execute the Python file
execute_main() {
    python3 main.py
}

# Function to stop the client and exit the script
stop_client() {
    pkill -f "python3 main.py"
    exit 0
}

# Main loop
while true; do
    echo "Select an option:"
    echo "1. Execute the client"
    echo "2. Stop the client"
    echo "3. Exit"
    read option

    case $option in
        1)
            execute_main
            ;;
        2)
            stop_client
            ;;
        3)
            exit 0
            ;;
        *)
            echo "Invalid option"
            ;;
    esac
done
