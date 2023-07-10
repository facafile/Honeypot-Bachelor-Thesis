import socket
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Server configuration
SERVER_HOST = '10.0.1.20'
SERVER_PORT = 8080
NODE_NAME = 'PHYSICAL'  # Replace with the actual node name
DIRECTORY = 'var/log/'

def send_log(log, file_path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
            message = f"{NODE_NAME} : {file_path} - {log}"  # Include the node name in the log message
            s.sendall(message.encode('utf-8'))
            print("Log sent successfully")
        except ConnectionRefusedError:
            print("Unable to connect to the server")


def send_new_logs(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            new_logs = f.read()
            send_log(new_logs, file_path)
    except UnicodeDecodeError:
        print("wrong encoding")
    except FileNotFoundError:
        print("File does not exist")
    
    

class LogFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            file_path = event.src_path
            send_new_logs(file_path)
    def on_created(self, event):
        return


def monitor_logs():
    event_handler = LogFileHandler()
    observer = Observer()
    observer.schedule(event_handler, DIRECTORY, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

# Usage example
if __name__ == '__main__':
    monitor_logs()

