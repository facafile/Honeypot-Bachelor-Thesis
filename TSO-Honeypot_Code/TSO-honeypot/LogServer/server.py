import socket
import os
from datetime import datetime

# Server configuration
HOST = '0.0.0.0'  # Listen on all network interfaces
PORT = 8080
LOGS_DIR = 'logs'  # Directory to store log files

def save_log(node_name, log):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {log}\n"
    file_path = os.path.join(LOGS_DIR, f"{node_name}.log")
    try:
        with open(file_path, 'a+') as f:
            f.write(log_entry)
            print(f"New log saved to {file_path}")
    except:
        print("could not save to log")

def start_server():
    # Create logs directory if it doesn't exist
    os.makedirs(LOGS_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(3)  # Allow up to 3 simultaneous connections
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr[0]}:{addr[1]}")

            # Receive and process logs from the client
            data = b""
            while True:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                data += chunk
            if data:
                log_data = data.decode('utf-8')
                log_parts = log_data.split(':', 1)
                if len(log_parts) == 2:
                    node_name, log = log_parts
                    print(f"Received log from {node_name}: {log}")
                    save_log(node_name, log)
                else:
                    print("Invalid log format")

            conn.close()

if __name__ == '__main__':
    start_server()

