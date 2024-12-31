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
    """
    Connect to the server at the specified address and port.
    Continually attempts to connect if the server is not found.
    
    Returns:
        socket: A connected client socket object.
    """
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
            time.sleep(1)  # Retry after 1 second
    return client_socket

def handle_server_disconnect(client_socket):
    """
    Handles the disconnection from the server.
    Closes the existing socket and re-establishes the connection.
    
    Returns:
        socket: A newly connected client socket object.
    """
    print("SERVER CONNECTION LOST, waiting for server connection...")
    client_socket.close()
    return connect_to_server()

def send_message(message, client_socket):
    """
    Sends a message to the server and waits for a response.
    If the server disconnects or fails, attempts to reconnect and resend the message.
    
    Args:
        message (str): The message to send to the server.
        client_socket (socket): The connected client socket object.

    Returns:
        str: The server's response message.
    """
    try:
        # Send the message to the server
        prot.send_all(data=message, socket=client_socket)
        # Receive the server's response
        response = prot.recv_all(socket=client_socket).decode('utf-8')
        return response
    except Exception:
        # Handle server disconnection by reconnecting and retrying the message
        client_socket = handle_server_disconnect(client_socket)
        return send_message(message, client_socket)  # Retry sending the message

def send_file(file_path, client_socket):
    """
    Sends a file to the server. If the server disconnects, it attempts to reconnect and resend the file.
    
    Args:
        file_path (str): The path of the file to send.
        client_socket (socket): The connected client socket object.
    """
    try:
        # Notify the server that a file is about to be sent
        client_socket.sendall(b"file")
        # Send the file to the server
        prot.send_file(socket=client_socket, file_name=file_path)
        # Wait for acknowledgment from the server
        ack = prot.recv_all(socket=client_socket).decode()
        if ack == "ACK":
            print("File was sent successfully")
    except (ConnectionRefusedError, ConnectionResetError):
        # Handle server disconnection and attempt to resend the file
        client_socket = handle_server_disconnect(client_socket)
        send_file(file_path, client_socket)  # Retry sending the file
    except Exception as e:
        print(f"[ERROR] Sending file failed: {e}")

def disconnect(client_socket):
    """
    Sends an 'exit' command to the server and closes the connection.
    
    Args:
        client_socket (socket): The connected client socket object.
    """
    try:
        # Send 'exit' to the server
        client_socket.sendall(b"exit")
        # Close the socket connection
        client_socket.close()
        print("[DISCONNECTED]")
    except Exception as e:
        print(f"[ERROR] Disconnection failed: {e}")

# API Functions

def connect():
    """
    API function to initiate the connection to the server.
    
    Returns:
        socket: A connected client socket object.
    """
    return connect_to_server()

def send_msg(message, client_socket):
    """
    API function to send a message to the server and receive a response.
    
    Args:
        message (str): The message to send to the server.
        client_socket (socket): The connected client socket object.

    Returns:
        str: The server's response message.
    """
    return send_message(message, client_socket)

def send_file_to_server(file_path, client_socket):
    """
    API function to send a file to the server.
    
    Args:
        file_path (str): The path of the file to send.
        client_socket (socket): The connected client socket object.
    """
    send_file(file_path, client_socket)

def disconnect_from_server(client_socket):
    """
    API function to disconnect from the server.
    
    Args:
        client_socket (socket): The connected client socket object.
    """
    disconnect(client_socket)

# Main Program Execution

if __name__ == "__main__":
    client_socket = connect_to_server()  # Connect to the server

    while True:
        try:
            user_input = input("Enter a command (message/send file/exit): ").lower()

            if user_input == "exit":
                disconnect(client_socket)
                break  # Exit the loop and disconnect
            elif user_input == "send file":
                while True:
                    file_path = input("Enter the file path to send: ")
                    if file_path == 'exit':
                        break  # Exit the file sending loop
                    if not os.path.exists(file_path):
                        print(f"[ERROR] File not found: \"{file_path}\". Try again!")
                        continue
                    send_file(file_path, client_socket)  # Send the file

            elif user_input:
                response = send_message(user_input, client_socket)  # Send message and receive response
                if response:
                    print("[RECEIVED]:", response)

        except (ConnectionRefusedError, ConnectionResetError):
            print("Server not found, waiting for server connection...")
            client_socket = handle_server_disconnect(client_socket)  # Reconnect to the server
        except Exception as e:
            print(e)
            break  # Exit on any unexpected errors
