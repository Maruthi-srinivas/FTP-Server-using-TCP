import socket
import ssl
import struct
import os
SERVER_HOST='127.0.0.1'
SERVER_PORT=1456
BUFFER_SIZE=1024
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '127.0.0.1'
    server_port = 12345

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with context.wrap_socket(client_socket, server_hostname=server_host) as ssl_client_socket:
        try:
            ssl_client_socket.connect((server_host, server_port))
            print(f"Connected to server at {server_host}:{server_port}")

            receive_file(ssl_client_socket)
        except Exception as e:
            print(f"Error: {e}")
def upload_file(file_name):
    if not os.path.exists(file_name):
        return "File does not exist."
    client_socket.send(b"UPLD")
    file_name_encoded=file_name.encode()
    client_socket.send(struct.pack("h".len(file_name_encoded))+file_name_encoded)
    file_size=os.path.getsize(file_name)
    client_socket.send(struct.pack("i",file_size))
    with open(file_name,"rb") as file:
        while True:
            bytes_read=file.read(BUFFER_SIZE)
            if not bytes_read:
                break
            client_socket.send(bytes_read)
    print(f"File {file_name} uploaded successfully")
    

def receive_file(client_socket):
    try:
        # Receive file size from the server
        file_size = int(client_socket.recv(1024).decode())
        print(f"File size: {file_size} bytes")

        received_data = b''
        while len(received_data) < file_size:
            data = client_socket.recv(1024)
            received_data += data

        # Ensure the 'requests' directory exists
        save_directory = 'requests'  # Directory name
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)  # Create the directory if it does not exist

        # Extract file extension from the received file path
        received_file_path = 'received_file'
        if file_size > 0:
            file_extension = os.path.splitext(received_file_path)[1]
            received_file_path = os.path.join(save_directory, received_file_path + file_extension)

        with open(received_file_path, 'wb') as file:
            file.write(received_data)

        print(f"File received and saved at {received_file_path}")
    except Exception as e:
        print(f"Error receiving file: {e}")

if __name__ == "_main_":
    start_client()