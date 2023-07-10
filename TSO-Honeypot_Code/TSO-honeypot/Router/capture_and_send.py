import subprocess
import socket
import select

# Define the remote server IP and port
server_ip = "10.0.1.20"
server_port = 8080

# Run tshark command to capture packets
tshark_command = ["tshark", "-i", "eth0", "-w", "-"]
process = subprocess.Popen(tshark_command, stdout=subprocess.PIPE)

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the remote server
    client_socket.connect((server_ip, server_port))
    print("Connected to the remote server.")

    # Set the socket in non-blocking mode
    client_socket.setblocking(0)

    while True:
        # Use select to check if there is data to read from tshark
        ready_sockets, _, _ = select.select([process.stdout], [], [], 0)
        if ready_sockets:
            # Read the captured packets from tshark output
            packet = ready_sockets[0].readline()
            packet = "ROUTER:" + packet.decode('utf-8')

            # Send the captured packet to the remote server
            client_socket.sendall(packet)

except ConnectionRefusedError:
    print("Connection to the remote server was refused.")

except KeyboardInterrupt:
    print("Script stopped by the user.")

finally:
    # Close the socket connection
    client_socket.close()
    # Terminate the tshark process
    process.terminate()
