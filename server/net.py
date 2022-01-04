import socket
from typing import Union

def start(host: str, port: int) -> socket.socket:
    """Initiate the server.
    Args:
        host (str): host server.
        port (int): port to connect to.

    Returns:
        socket object
    """    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,port))
    sock.listen()
    return sock

def write(socket: socket.socket, data: str):
    """Write data into the socket.
    
    Args:
        socket (socket): socket to use when writing.
        data (str): data to write.
    """    
    socket.sendall(data.encode())

def read(socket: socket.socket) -> str:
    """Read data from the socket.

    Args:
        socket (socket): socket to use when reading.

    Returns:
        str: data read from socket.
    """
    return socket.recv(1024).decode()

def close(socket: socket.socket):
    """Close socket.

    Args:
        socket (socket): socket to close.
    
    Returns:
        None if successful.
    """    
    # simulates waiting time of server response
    # mainly used for testing the typing animation
    return socket.close()