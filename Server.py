import socket
import Protocol as prot
from Protocol import HEADER_SIZE
import subprocess

# Constants
HOST = 'localhost'
PORT = 9098
ADDR = (HOST, PORT)
BUF_SIZE = 1024
PAINT_PATH = r"C:\Windows\System32\mspaint.exe"
MEDIA_PLAYER = r"C:\Users\Ilan\Documents\wmplayer.exe"

# Function to bind server and wait for client connection
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDR)
    server_socket.listen(5)
    print(f"Server Ready, Waiting for client on {ADDR}")
    client_socket, client_addr = server_socket.accept()
    print(f"New client connected on {client_addr}")
    return server_socket, client_socket, client_addr

# Function to handle client disconnection
def handle_client_disconnect(server_socket):

    print("Server socket closed.")
    return start_server()

# Function to handle file requests from the client
def handle_file_request(client_socket):
    file_name = prot.recv_file(socket=client_socket)
    if file_name:
        if file_name.lower().endswith(('.jpg', '.png', '.gif')):
            subprocess.run([PAINT_PATH, file_name])

        elif file_name.lower().endswith(('.mp3', '.mp4')):
            subprocess.run([MEDIA_PLAYER, file_name])

        ACK = "ACK"
        prot.send_all(data=ACK, socket=client_socket)
        print(f"[SEND TO CLIENT]: {ACK}")


# Function to manage communication with the client
def manage_client_connection():
    # Start server and wait for client connection
    server_socket, client_socket, client_addr = start_server()

    while True:
        try:
            data = client_socket.recv(BUF_SIZE)

            if not data:
                client_socket.close()
                # No data received, handle disconnect
                client_socket, client_addr = server_socket.accept()
                continue

            elif data.decode() == 'exit':
                break

            if data.decode().lower() == "file":
                handle_file_request(client_socket)

            elif data:
                print(f"[RECEIVED FROM CLIENT AT] {client_addr}: {data[HEADER_SIZE:].decode('utf-8')}")
                client_socket.sendall(data)
                print(f"[SEND TO CLIENT]: {data[HEADER_SIZE:].decode()}")

        except Exception as e:
            print(f"[ERROR]: {e}")
            break

    # Closing connection after interaction
    input("Press any key to close")
    server_socket.close()
    client_socket.close()

if __name__ == "__main__":
    manage_client_connection()
