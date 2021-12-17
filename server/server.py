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
HOST = "127.0.0.1" #localhost
PORT = 3000
def server() :
    net.start()
    
    pass
if __name__ == "__main__":
    server()
