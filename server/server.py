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
import net
import concurrent.futures
import logging
from security import authenticate

HOST = "127.0.0.1" #localhost
PORT = 3000
def server() :
    logging.basicConfig(filename="logs/server.log",filemode="w",level=20, format='%(asctime)s:%(levelNAME)s:%(NAME)s:%(message)s')

    # start the server
    net.current_socket = net.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as exec:
        # get the connection from a client
        conn, addr = net.current_socket.accept()
        logging.info(f"Connected by {addr}")

        # verify the token to start the chat
        authenticate(conn)

        # ready to listen for the client requests
        while True :
            request = net.read(conn)
            # process the request here
         
if __name__ == "__main__":
    server()
