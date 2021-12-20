import socket
import net
from animation import animate_typing
from security import authenticate
import concurrent.futures
import logging

HOST = "127.0.0.1" #localhost
PORT = 3000
MAX_ATTEMPTS = 3
TIMEOUT = 60 #seconds

def cli():
    logging.basicConfig(filename="logs/client.log",filemode="w",level=20, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    # Initialize connection to the host
    # only done on start and we keep it open
    # until we are done
    net.current_socket = net.connect(HOST, PORT)
    
    try:
        if net.current_socket is None:
            print(f"Server Unavailable. Try again later!")
            exit()
    
        net.current_socket.settimeout(TIMEOUT)

        print(f"Connection Timeout after {TIMEOUT} seconds of inactivity.")
        NAME, EMAIL, OK = authenticate(MAX_ATTEMPTS)

        if not OK:
            print(f"Unauthorized. Try again later!")
            net.close(net.current_socket)
            exit()

        # make requests on another thread to make animations
        # on the main thread
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as exec:
            print(f"Chatbot: hi {NAME}. Ask me anything!")
            # chat loop
            while True:
                # wait for user input
                text = input(f"{NAME}: ")
                if text == "":
                    break

                net.write(net.current_socket, text)

                # start waiting for response on the other thread
                # freeing up the main one for animation
                response = exec.submit(net.read, net.current_socket)

                while not response.done():
                    animate_typing()

                if response.result().lower() == "bye!":
                    net.close(net.current_socket)
                    print(f"Chatbot: bye!", flush=True)
                    exit()
                else:
                    print(f"Chatbot: {response.result()}", flush=True)
    
    except Exception:
        print("Timeout!", flush=True)
    finally:
        net.close(net.current_socket)
        exit()

if __name__ == "__main__":
    cli()