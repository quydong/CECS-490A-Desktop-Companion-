import socket

# Create a socket object using the IPv4 address family and TCP protocol
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get the hostname of the Windows laptop
host = socket.gethostname()

# Choose a port for the server that is not used by any standard service
port = 12345

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections (the argument is the backlog of allowed connections)
server_socket.listen(5)

print(f"Server running on {host}:{port}. Waiting for connections...")

while True:
    # Accept an incoming connection
    client_socket, addr = server_socket.accept()
    print(f"Got a connection from {addr}")

    # Send a message to the connected client
    message = 'Hello from the server!'
    client_socket.send(message.encode('utf-8'))

    # Close the connection with the client
    client_socket.close()

    # Break the loop if you want to accept only one connection
    # Remove or comment out the break statement to keep listening for incoming connections
    break
