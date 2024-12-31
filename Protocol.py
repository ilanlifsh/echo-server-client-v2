import os  # Import the os module for file handling

# Constants for message header size, buffer size, and file header size
HEADER_SIZE = 10
BUF_SIZE = 2
FILE_HEADER = 20

# Function to send all data through the socket
def send_all(**kwargs):
    # Retrieve socket and data from keyword arguments
    socket = kwargs.get("socket")
    data = kwargs.get("data")
    
    # Create the header which indicates the length of the data
    header = str(len(data))

    # Right-justify the header to ensure it's of fixed size (HEADER_SIZE)
    msg = header.rjust(HEADER_SIZE, '0') + data

    # Send the message through the socket
    socket.sendall(msg.encode())

# Function to receive all data from the socket
def recv_all(**kwargs):
    try:
        # Retrieve the socket from keyword arguments
        socket = kwargs.get("socket")
        
        # Receive the header (the length of the message)
        msg_len = int(socket.recv(HEADER_SIZE).decode())

        msg_data = b''  # Initialize an empty byte string to store the received data

        # Receive data in chunks of size BUF_SIZE until the full message is received
        while len(msg_data) < msg_len:
            msg_data += socket.recv(BUF_SIZE)
        
        # If no data is received, raise an exception
        if msg_data == b'':
            raise Exception
        
        # Return the received message data
        return msg_data
    except:
        # If an exception occurs (e.g., socket error), return an empty byte string
        return b''

# Function to send a file to the client
def send_file(**kwargs):
    # Retrieve the socket and file name from keyword arguments
    client_socket = kwargs.get('socket')
    file_name = kwargs.get('file_name')
    
    # Open the file in read-binary mode
    file = open(file_name, 'rb')
    
    # Get the size of the file and right-justify it to HEADER_SIZE
    file_size = str(os.path.getsize(file_name)).rjust(HEADER_SIZE, '0')
    
    # Right-justify the file name to FILE_HEADER size
    file_name_padded = os.path.basename(file_name).rjust(FILE_HEADER, ' ')
    
    # Send the file size and file name to the client
    client_socket.sendall(file_size.encode())
    client_socket.sendall(file_name_padded.encode())

    data_sent = 0  # Keep track of the amount of data sent

    # Read the file in chunks and send it to the client
    file_size = int(file_size)  # Convert the file size to an integer
    while data_sent < file_size:
        rxd = file.read(BUF_SIZE)  # Read a chunk of the file
        client_socket.sendall(rxd)  # Send the chunk to the client
        data_sent += len(rxd)  # Update the amount of data sent

    file.close()  # Close the file after sending

# Function to receive a file from the client
def recv_file(**kwargs):
    try:
        # Retrieve the socket from keyword arguments
        client_socket = kwargs.get('socket')
        
        # Receive the file size from the client
        file_size = int(client_socket.recv(HEADER_SIZE).decode())
        
        # Receive the file name from the client
        file_name = (client_socket.recv(FILE_HEADER).decode()).strip()

        # If file name or size is invalid, return None
        if file_name == "" or not file_size:
            return None

        # Create a folder named "upload" to store the received files, if it doesn't exist
        folder_path = os.path.join(os.getcwd(), "upload")
        if not os.path.exists(folder_path):
            os.mkdir("upload")

        # Set the full file path for saving the received file
        file_name = os.path.join(folder_path, file_name)

        # Open the file in write-binary mode
        with open(file_name, 'wb') as file:
            data_recv = 0  # Keep track of the amount of data received

            # Receive the file in chunks and write it to the file
            while data_recv < file_size:
                line = client_socket.recv(BUF_SIZE)
                file.write(line)  # Write the received data to the file
                data_recv += len(line)  # Update the amount of data received

        return file_name  # Return the path to the saved file

    except:
        # If any error occurs (e.g., file not received correctly), return None
        return None
