
# Project Overview

This project implements a basic client-server communication system where the client can send messages or files to the server. The server can process incoming messages and files, and the client can receive responses from the server. The server can also launch external applications (like Paint and Windows Media Player) when receiving certain types of files (such as images and media files).

## Project Structure

### 1. `client.py`

The client-side code handles:

- Connecting to the server
- Sending messages or files
- Handling server disconnections and retries
- Sending exit signals to gracefully close the connection

### 2. `server.py`

The server-side code handles:

- Listening for client connections
- Receiving and responding to messages
- Receiving and processing files (like images and media files)
- Launching external applications (e.g., Paint, Windows Media Player)

### 3. `Protocol.py`

Contains the communication protocol for the client-server interaction. This includes:

- Sending and receiving messages with headers
- Sending and receiving files, including handling file headers and sizes
- Managing socket communication in a reliable manner

---

# Usage

### Client:

1. To run the client, execute the following command:

    ```bash
    python client.py
    ```

2. The client will attempt to connect to the server. Once connected, you can send messages or files.
    - To send a message, simply type your message and press enter.
    - To send a file, type `send file`, then provide the file path when prompted.
    - To exit the client, type `exit`.

### Server:

1. To run the server, execute the following command:

    ```bash
    python server.py
    ```

2. The server will wait for client connections and handle messages and files received from the client.

### Protocol Handling:

The `Protocol.py` file provides the necessary functions for:

- `send_all(data, socket)` – Sends data with a header to the socket.
- `recv_all(socket)` – Receives data from the socket, managing the header and message length.
- `send_file(socket, file_name)` – Sends a file through the socket, including file size and name.
- `recv_file(socket)` – Receives a file from the socket and saves it locally.

---

# File Handling

- **Sending Files**: The client can send files of various types (e.g., `.jpg`, `.png`, `.mp3`, `.mp4`).
- **Receiving Files**: The server can process files such as images (opened in Paint) and media files (opened in Windows Media Player).

---

# Requirements

- Python 3.x
- `os`, `socket`, `Protocol` modules (ensure `Protocol.py` is in the same directory as `client.py` and `server.py`)

---

# License

This project does not have an MIT License or any specific licensing. You may use or modify the code as you wish
