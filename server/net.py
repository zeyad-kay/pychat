import socket
import logging

def start(host: str, port: int):
    """Initiating the sever.
    Args:
        host (str): host server.
        port (int): port to connect to.

    Returns:
        None.
    """    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,port))
    sock.listen()

def write(socket: socket.socket, data: str):
    """Write data into a socket.
    
    Args:
        socket (socket): socket to use when writing.
        data (str): data to write.
    """    
    socket.sendall(data.encode())

def read(socket: socket.socket):
    """Read data from a socket

    Args:
        socket (socket): socket to use when reading.

    Returns:
        str: data read from socket.
    """    
    # simulates waiting time of server response
    # mainly used for testing the typing animation
    return socket.recv(1024).decode()
