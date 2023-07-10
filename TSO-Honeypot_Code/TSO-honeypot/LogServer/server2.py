import socket

# Define the server IP address and port
server_ip = "0.0.0.0"
server_port = 8081

# Create a TCP socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server IP and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen(1)
print("Log receiver server is listening on {}:{}".format(server_ip, server_port))

# Open the log file in append mode
with open("logs/in.log", "a+") as log_file:
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from {}:{}".format(client_address[0], client_address[1]))

        # Receive and process log messages
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Process log messages as needed
            try:
                # Attempt to decode data as UTF-8
                decoded_data = data.decode('utf-8')
                log_file.write(decoded_data + "\n")  # Write the log entry to the file
            except UnicodeDecodeError:
                # Write the raw byte data to the file
                log_file.write("{}\n".format(data))

        # Close the client socket connection
        client_socket.close()

