#!/bin/bash

# Function to check if the connection is open
check_connection() {
  while ! nc -z 10.0.1.20 8081; do
    sleep 1
  done
}

# Call the function to wait for the connection
check_connection

# Once the connection is open, run the tshark command
tshark -i eth0 -w - | nc 10.0.1.20 8081

