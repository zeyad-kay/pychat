import socket
import logging

def connect(host: str, port: int):
    """Connect to a server on specified host and port.

    Args:
        host (str): host server.
        port (int): port to connect to.

    Returns:
        socket object. None if unsuccessful.
    """    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except Exception as e:
        logging.error(e)
        sock = close(sock)
    finally:
        return sock

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
