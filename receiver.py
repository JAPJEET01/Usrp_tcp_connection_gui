import socket

# Server socket settings
host = 'localhost'
port = 12345  # Make sure this matches the port used in server.py

try:
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((host, port))

    # Command to run on the server
    command = "python /home/usrp/Desktop/control.py"

    # Send the command
    client_socket.sendall(command.encode('utf-8'))

    # Receive the response from the server (if any)
    response = client_socket.recv(4096).decode('utf-8')
    print(f"Server response: {response}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the socket
    client_socket.close()
