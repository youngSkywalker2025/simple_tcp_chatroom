import threading
import socket
# Socket is the endpoint of a communication channel between two servers (server and client)

host = '127.0.0.1' #localhost
port = 55555
# Create Socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # (Kind of socket-> Internet Socket, Protocol -> TCP).
server.bind((host, port))
server.listen() # server starts listening for incoming connections 


clients = []
nicknames = []


# 3 methods needed: 

# Broadcast method: this sends a message to all connected clients 
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle Method: this runs for each client, listening for incoming messages. If a client disconnects, it cleans up
def handle(client):
    while True: 
        try: # as long as it works without giving you an exception or error
            message = client.recv(1024) # as long as it works that we recieve a message from the client 
            broadcast(message) # we are going to broadcast the message to all the other clients 
        except: # get some error
            # Remove client on disconnect
            index = clients.index(client) #finds the position of the current client in that list
            clients.remove(client) # removes the client's socket from the clients list
            client.close() # closes the tcp connection properly to free resources 
            nickname = nicknames[index] # uses the same index you found earlier to grab the nickname associated with this client from the nicknames likst
            broadcast(f'{nickname} left the chat!'.encode('utf-8')) # notifies all remaining clients that this person left the chat (Sends message to every connected client)
            nicknames.remove(nickname) # cleans up the nickname list so its stays in sync with the clients list 
            break

# Main loop of the server - its always waiting for new clients to join
def receive():
    while True:
        client, address = server.accept() # waiting until a client connects
        print(f"connected with {str(address)}")

        client.send("NICK".encode('utf-8')) # ask client for nickname,... needed because sockets trasmit bytes 
        nickname = client.recv(1024).decode('utf-8') # waits for the client to reply with their nickname,... converts it back to a string
        nicknames.append(nickname) # saves both the client and nickname into parallel lists: nickname holds strings
        clients.append(client) # clients holds sockets

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".decode('utf-8')) # sends a message to all existing clients that a new user joined 
        client.send("Connected to the server!".encode('utf-8')) # sends a private welcome message back to the new client
        
        thread = threading.Thread(target=handle, args=(client,)) # creates a new thread dedicated to handling this client's messages,... runs the handle(client) function for this specific client  
        thread.start() # runs the thread in the background 




# The main process = chat server
# each thread = a waiter assigned to a specific client
    # one thread handles alice's messages
    # another handles bob's etc. 
# since the threads run in parallel, the server can listen to all clients at once, instead of one at a time. 
# threads share the same resources (memory space)