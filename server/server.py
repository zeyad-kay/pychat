''''
This is the server module. First, initialize the main socket then bind
it to the host and port specified in client.py, start listening, then
enter the server loop.

Inside the server loop start accepting connections and read ALL the data.
You will probably have to loop until there is no data in the buffer.
After proccessing the request, send the response. Unlike reading, you can
send the response without looping by calling sendall.

All of the above was for handling one request only. To handle multiple
requests at the same time, you have 2 options:

1. Make every request in its own thread by wrapping the while loop
into a ThreadPoolExecutor() like the one in the client, and specify
the max number of concurrent connections or threads, make
it 3 or 4 to prevent overloading your device. 

2. Make requests asynchronous like Node.js, you will have to set the sockets
as non blocking and use the asyncio module that provides some helpers.
(Ignore this if you haven't used Node.js or you don't have time.)
'''
import socket
import net
import concurrent.futures
import logging
from security import authenticate
import time
import os
import mail
import mongo

HOST = "127.0.0.1" #localhost
PORT = 3000
MAX_ATTEMPTS = 3

def handler(socket: socket.socket, ipaddress):
    try:
        # verify the token to start the chat
        OK = authenticate(socket, MAX_ATTEMPTS)

        if OK:
            # chat loop
            while True :
                data = net.read(socket)
                print("sleep...")
                time.sleep(3)
                print("send...")
                net.write(socket, "Data from server")
    except ValueError:
        pass
    except Exception as e:
        logging.error(e)
    finally: 
        logging.info(f"{ipaddress} disconnected.")
        net.close(socket)
        return

def server() :
    logging.basicConfig(filename="logs/server.log",filemode="w",level=20, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    # start the server
    socket = net.start(HOST, PORT)
    try:
        mongo.db = mongo.connect()
        mail.server = mail.connect()
    except Exception as e:
        print(e)
        exit()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as exec:
        while True:
            conn, addr = socket.accept()
            # get the connection from a client
            logging.info(f"{addr[0]} connected.")
            # handle client in a new thread
            exec.submit(handler, conn, addr[0])
 
if __name__ == "__main__":
    server()
