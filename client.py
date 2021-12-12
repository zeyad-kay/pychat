import socket
from utils import *
import concurrent.futures

HOST = "127.0.0.1" #localhost
PORT = 3000

def connect(host, port):
    '''
    Create the socket and connect it to the server on the specified host and port
    then return it.
    '''
    return

def write(socket, data):
    '''
    Write data into the socket using sendall
    '''
    return

def read(socket):
    '''
    Read data into the socket using recv. You will have to loop until all bytes have been
    read.
    '''
    # simulates waiting time of server response
    # mainly used for testing the typing animation
    simulate_delay(1.5)
    return "Data from server."

def main():
    # Initialize connection to the host
    # only done once on start and we keep it open
    # until we are done
    sock = connect(HOST, PORT)
    
    # make requests on another thread to make animations
    # on the main thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as exec:
        # chat loop
        while True:
            # wait for user input
            text = input("User: ")

            if text == "exit":
                # close socket before returning
                return

            # write input to socket
            write(sock, text)

            # start waiting for response on the other thread
            # freeing up the main one for animation
            response = exec.submit(read, sock)
            while not response.done():
                animate_typing()

            print(f"Chatbot: {response.result()}", flush=True)

if __name__ == "__main__":
    main()