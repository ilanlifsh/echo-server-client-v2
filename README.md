# Server-Client Communication with File Handling

This project implements a server and client communication system using TCP sockets. The server listens for client connections and handles messages or file transfers from clients. It also allows the client to request media files to be opened with specific applications (e.g., Paint or Windows Media Player).

## Overview

The project includes two main components:

1. **Server (`server.py`)**: 
    - Accepts incoming client connections.
    - Processes client messages.
    - Handles file transfers (image and audio/video).
    - Executes media applications based on file types (Paint for images, Windows Media Player for audio/video).
    - Allows for disconnections and reconnections.

2. **Protocol (`Protocol.py`)**: 
    - Handles communication between the client and server (sending and receiving data).
    - Provides functions for sending and receiving files over the network.

3. **Client (`client.py`)**: 
    - Connects to the server, sends messages, and handles file transfers.
    - Automatically retries connecting to the server in case of disconnect.
    - Supports file sending and receiving server responses.

### Features

- **Server**:
  - Listens on a specified address and port for client connections.
  - Handles incoming messages and file requests from clients.
  - Executes media files (images and videos/audio) using external applications (e.g., Paint, Windows Media Player).
  - Sends ACK responses back to the client.
  
- **Client**:
  - Connects to the server and can send text messages or files.
  - Requests the server to open media files (images, audio, video).
  - The client sends a "file" command to upload files to the server.
  - Supports automatic reconnection if the server is disconnected.

### Key Modules

1. **`server.py`**:
    - `start_server()`: Initializes the server, binds it to an address, and waits for client connections.
    - `handle_client_disconnect()`: Handles client disconnection and restarts the server if needed.
    - `handle_file_request()`: Processes requests for file transfers, opening images with Paint or media files with Windows Media Player.
    - `handle_client_message()`: Handles and processes received messages from the client.
    - `manage_client_connection()`: Main loop that manages the communication between the server and the client.
  
2. **`Protocol.py`**:
    - `send_all()`: Sends a message with a header that includes the message length.
    - `recv_all()`: Receives a message and reconstructs it.
    - `send_file()`: Sends a file to the client.
    - `recv_file()`: Receives a file from the client and saves it to disk.

3. **`client.py`**:
    - `connect_to_server()`: Connects to the server and automatically retries if the connection fails.
    - `handle_server_disconnect()`: Handles server disconnects and automatically reconnects.
    - `send_message()`: Sends text messages to the server and receives the server’s response.
    - `send_file()`: Sends a file to the server.
    - `disconnect()`: Disconnects the client from the server.

## Requirements

- Python 3.x

## Setup and Usage

### Running the Server

1. **Run the server**:
   To start the server, run the `server.py` script:
   ```bash
   python server.py
   
###  Running the Client:

1. To run the client, execute the following command:

    ```bash
    python client.py
    ```
