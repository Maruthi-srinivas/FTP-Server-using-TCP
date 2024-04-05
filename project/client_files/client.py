import socket
import struct
import os
import ssl

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1456
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_context=ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations("server-cert.pem")

def connect_to_server():

    s.connect((SERVER_HOST, SERVER_PORT))
    conn=ssl_context.wrap_socket(s,server_hostname="deepak")
    print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")
    return conn

def upload_file(file_name,s):
    if not os.path.exists(file_name):
        print("File does not exist")
        return
    s.send(b"UPLD")
    file_name_encoded = file_name.encode()
    s.send(struct.pack("h", len(file_name_encoded)) + file_name_encoded)
    file_size = os.path.getsize(file_name)
    s.send(struct.pack("i", file_size))
    with open(file_name, "rb") as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.send(bytes_read)
    print(f"File {file_name} uploaded successfully")

def download_file(file_name,s):
    s.send(b"DWLD")
    file_name_encoded = file_name.encode()
    s.send(struct.pack("h", len(file_name_encoded)) + file_name_encoded)
    file_size = struct.unpack("i", s.recv(4))[0]
    if file_size == -1:
        print("File not found on server")
        return
    with open(file_name, "wb") as file:
        bytes_received = 0
        while bytes_received < file_size:
            bytes_read = s.recv(BUFFER_SIZE)
            if not bytes_read:
                break  # Connection closed
            file.write(bytes_read)
            bytes_received += len(bytes_read)
    print(f"File {file_name} downloaded successfully")

def list_files(s):
    s.send(b"LIST")
    count = struct.unpack("i", s.recv(4))[0]
    print("Files on server:")
    for _ in range(count):
        file_name_length = struct.unpack("i", s.recv(4))[0]
        file_name = s.recv(file_name_length).decode()
        print(f"- {file_name}")

def delete_file(file_name,s):
    s.send(b"DELF")
    file_name_encoded = file_name.encode()
    s.send(struct.pack("h", len(file_name_encoded)) + file_name_encoded)
    result = s.recv(1)
    if result == b"1":
        print(f"File {file_name} deleted successfully")
    else:
        print("File not found on server")

def main():
    conn=connect_to_server()
    while True:
        cmd = input("Enter command (UPLD, DWLD, LIST, DELF, QUIT): ").upper()
        if cmd == "UPLD":
            file_name = input("Enter filename to upload: ")
            upload_file(file_name,conn)
        elif cmd == "DWLD":
            file_name = input("Enter filename to download: ")
            download_file(file_name,conn)
        elif cmd == "LIST":
            list_files(conn)
        elif cmd == "DELF":
            file_name = input("Enter filename to delete: ")
            delete_file(file_name,conn)
        elif cmd == "QUIT":
            s.close()
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
