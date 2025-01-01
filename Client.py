import socket
import Protocol as prot
import os
import time

# Constants
HOST = 'localhost'
PORT = 9098
ADDR = (HOST, PORT)
BUF_SIZE = 2


def connect_to_server():
    connected = False
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'[CONNECTING] Connecting to server at {ADDR[0]}:{ADDR[1]} ...')
    while not connected:
        try:
            client_socket.connect(ADDR)
            connected = True
            print("[CONNECTED]")
        except Exception as e:
            print("Server not found, retrying...")
            time.sleep(1)
    return client_socket
def handle_server_disconnect(client_socket):
    print("SERVER CONNECTION LOST, waiting for server connection...")
    client_socket.close()
    connect_to_server()

def send_message(message, client_socket):
    try:
        prot.send_all(data=message, socket=client_socket)
        response = prot.recv_all(socket=client_socket).decode('utf-8')
        return response
    except Exception:
        handle_server_disconnect(client_socket)


def send_file(file_path, client_socket):

    try:
        client_socket.sendall(b"file")
        prot.send_file(socket=client_socket, file_name=file_path)
        ack = prot.recv_all(socket=client_socket).decode('utf-8')
        if ack == "ACK":
            print("File was sent successfully")
    except (ConnectionRefusedError, ConnectionResetError):
        handle_server_disconnect(client_socket)

    except Exception as e:
        print(f"[ERROR] Sending file failed: {e}")

def disconnect(client_socket):
    try:
        client_socket.sendall(b"exit")
        client_socket.close()
        print("[DISCONNECTED]")
    except Exception as e:
        print(f"[ERROR] Disconnection failed: {e}")


if __name__ == "__main__":
    client_socket = connect_to_server()

    while True:
        try:
            user_input = input("Enter a command (message/send file/exit): ").lower()

            if user_input == "exit":
                disconnect(client_socket)
                break
            elif user_input == "send file":
                while True:
                    file_path = input("Enter the file path to send: ")
                    if file_path == 'exit':
                        break
                    if not os.path.exists(file_path):
                        print(f"[ERROR] File not found: \"{file_path}\". Try again!")
                        continue
                    send_file(file_path, client_socket)

            elif user_input:
                response = send_message(user_input,client_socket)
                if response:
                    print("[RECEIVED]:", response)


        except (ConnectionRefusedError, ConnectionResetError):
            print("Server not found, waiting for server connection...")
            handle_server_disconnect(client_socket)
        except Exception as e:
            print(e)
            break
