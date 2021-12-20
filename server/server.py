''''
This is the server module. First, initialize the main socket then bind
it to the host and port specified in client.py, start listening, then
enter the server loop.

Inside the server loop start accepting connections and read ALL the data.
You will probably have to loop until there is no data in the buffer.
After proccessing the request, send the response. Unlike reading, you can
send the response without looping by calling sendall.

All of the above was for handling one request only. To handle multiple
requests at the same time, you have to make every request in its own thread by wrapping the while loop
into a ThreadPoolExecutor() like the one in the client, and specify
the max number of concurrent connections or threads, make
it 3 or 4 to prevent overloading your device. 
'''
import socket
from socket import timeout
import net
import concurrent.futures
import logging
from security import authenticate
import time
import os
import mail
import mongo
import chatbot
import sys

HOST = "127.0.0.1" #localhost
PORT = 3000
MAX_ATTEMPTS = 3
TIMEOUT = 60 #second(s)

def handler(socket: socket.socket, ipaddress: str):
    """Client connection handler.

    Args:
        socket (socket.socket): client connection socket.
        ipaddress (str): client IP address.
    """    
    chat = ''
    try:
        # verify the token to start the chat
        email, OK = authenticate(socket, MAX_ATTEMPTS)

        if OK:
            # chat loop
            while True :
                msg = net.read(socket)
                if msg != "":
                    resp = chatbot.get_response(msg)
                    chat += f"User: {msg}\nChatbot:{resp}\n"
                    time.sleep(2)
                    net.write(socket, resp)
                else:
                    break
    except ValueError:
        pass
    except timeout as e:
        pass
    except Exception as e:
        logging.error(e)
    finally:
        # save to db if there was a chat
        if len(chat):
            mongo.db["chats"].insert_one({ "chat": chat.rstrip("\n"), "email": email })
    
        logging.info(f"{ipaddress} disconnected.")
        net.close(socket)
        return

def server():
    logging.basicConfig(filename="logs/server.log",filemode="w",level=20, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

    # start the server
    # connect mongodb and mail servers
    try:
        sock = net.start(HOST, PORT)
        logging.info(f"Server listening on port {PORT}.")
        mongo.db = mongo.connect()
        logging.info("MongoDB server connected.")
        mail.server = mail.connect()
        logging.info("Mail server connected.")
    except Exception as e:
        logging.error(e)
        net.close(sock)
        exit()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as exec:
        while True:
            conn, addr = sock.accept()
            conn.settimeout(TIMEOUT)
            logging.info(f"{addr[0]} connected.")
            # handle client in a new thread
            exec.submit(handler, conn, addr[0])

def envvars(filename: str):
    """Parse environment variables from a file.

    Args:
        filename (str): File containing environment variables.
    """    
    with open(filename, "r") as f:
        for l in f.readlines():
            k, v = l.split("=", 1)
            os.environ[k.strip()] = v.strip()

if __name__ == "__main__":
    try:
        envvars(sys.argv[1])
        server()
    except IndexError:
        print("Must provide environment variables file.")
    except Exception as e:
        print(e)
