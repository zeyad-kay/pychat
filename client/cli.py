import net
from animation import animate_typing
from security import authenticate
import concurrent.futures
import logging

HOST = "127.0.0.1" #localhost
PORT = 3000
MAX_ATTEMPTS = 3
BLOCK_TIME = 5 #minutes
def cli():
    logging.basicConfig(filename="logs/client.log",filemode="w",level=20, format='%(asctime)s:%(levelNAME)s:%(NAME)s:%(message)s')

    # Initialize connection to the host
    # only done on start and we keep it open
    # until we are done
    net.current_socket = net.connect(HOST, PORT)
    if net.current_socket is None:
        print(f"Server Unavailable. Try again in {BLOCK_TIME} minutes.!")
        exit()

    NAME, EMAIL, OK = authenticate(MAX_ATTEMPTS)

    if not OK:
        print(f"Try again in {BLOCK_TIME} minutes!")
        net.current_socket.close()
        exit()

    # make requests on another thread to make animations
    # on the main thread
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as exec:
        print(f"Chatbot: Hi {NAME}!")
        # chat loop
        while True:
            # wait for user input
            text = input(f"{NAME}: ")

            if text == "exit" or text == "bye":
                net.current_socket.close()
                print(f"Chatbot: bye!", flush=True)
                exit()

            net.write(net.current_socket, text)

            # start waiting for response on the other thread
            # freeing up the main one for animation
            response = exec.submit(net.read, net.current_socket)
            while not response.done():
                animate_typing()

            print(f"Chatbot: {response.result()}", flush=True)

if __name__ == "__main__":
    cli()