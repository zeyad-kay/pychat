import socket
from utils import *
import logging
import asyncio

HOST = "127.0.0.1" #localhost
PORT = 3000

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
        sock = sock.close()
    finally:
        return sock

def write(socket: socket.socket, data: str):
    """Write data into a socket.
    
    Args:
        socket (socket): socket to use when writing.
        data (str): data to write.
    """    
    socket.sendall(data.encode())

async def read(socket: socket.socket):
    """Read data from a socket

    Args:
        socket (socket): socket to use when reading.

    Returns:
        str: data read from socket.
    """    
    msg = socket.recv(1024).decode()

    # simulates waiting time of server response
    # mainly used for testing the typing animation
    await simulate_delay(0.5)
    return msg

async def main():
    logging.basicConfig(filename="logs/client.log",filemode="w", level=20, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    # Initialize connection to the host
    # only done on start and we keep it open
    # until we are done
    sock = connect(HOST, PORT)
    if sock is None:
        print("Server Unavailable. Try Again!")
        exit()
    
    # chat loop
    while True:
        # wait for user input
        text = input("User: ")
        
        if text == "exit" or text == "bye":
            sock.close()
            print(f"Chatbot: bye!", flush=True)
            exit()
        
        write(sock, text)
        
        # asynchronously read the response to make animations.
        # Equivalent to Promises in Javascript.
        task = asyncio.create_task(read(sock))

        while not task.done():
            await animate_typing()
        
        print(f"Chatbot: {task.result()}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())