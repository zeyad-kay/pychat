import socket
from utils import *
import concurrent.futures

HOST = "127.0.0.1" #localhost
PORT = 3000

def connect(host, port):
    return

def write(socket, data):
    return

def read(socket):
    # simulates waiting time of server
    simulate_delay(1.5)
    return "Data from server."

def main():
    # Initialize connection to the host
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