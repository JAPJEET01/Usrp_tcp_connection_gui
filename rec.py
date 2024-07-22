import socket

# TCP server configuration (Sender's TCP server)
TCP_HOST = 'localhost'  # Replace with sender's IP if not localhost
TCP_PORT = 6000

# Function to connect to TCP server and receive data
def tcp_client():
    try:
        # Create TCP client socket
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client_socket.connect((TCP_HOST, TCP_PORT))
        print(f"Connected to TCP server at {TCP_HOST}:{TCP_PORT}")

        # Receive and print data
        while True:
            data = tcp_client_socket.recv(1024)
            if not data:
                break
            print(f"Received data: {data.decode('utf-8').strip()}")

    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        if 'tcp_client_socket' in locals():
            tcp_client_socket.close()

if __name__ == "__main__":
    tcp_client()
