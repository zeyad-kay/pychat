import socket
import logging

def start(host: str, port: int):
    """Initiating the sever.
    Args:
        host (str): host server.
        port (int): port to connect to.

    Returns:
        socket object. None if unsuccessful.
    """    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host,port))
    sock.listen()
    return sock

def write(connection, data: str):
    """Write data into a connection.
    
    Args:
        socket (socket): socket to use when writing.
        data (str): data to write.
    """    
    connection.sendall(data.encode())

def read(connection):
    """Read data from a connection

    Args:
        socket (socket): socket to use when reading.

    Returns:
        str: data read from socket.
    """    
    # simulates waiting time of server response
    # mainly used for testing the typing animation
    return connection.recv(1024).decode()
