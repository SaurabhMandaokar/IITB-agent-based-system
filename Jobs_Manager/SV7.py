import json
import socket
import threading
from BaseLibraries.messaging import flatten, unflatten
from BaseLibraries.messaging import dummyFIPA


host = "localhost"  # localhost --or-- put device IP address
port = 6525

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()  # server start listening for connections

clients = []
nicknames = []


# broadcasting message to all the clients
def broadcast(message):
    for client in clients:
        client.send(message)


def forward_to_receivers(message):
    msg = unflatten(message)
    print(f"sending {msg.performative} to {msg.receiver}")
    if msg.protocol != "DUMMY_FIPA":
        try:
            for n_name in eval(msg.receiver):

                nickname_index = nicknames.index(n_name)
                clients[nickname_index].send(message)
        except:
            nickname_index = nicknames.index(msg.receiver)
            clients[nickname_index].send(message)


def handle(client):
    print("initial tasks done")
    while True:
        message = client.recv(1024)
        if len(message) > 0:
            msg = message
            while len(message) > 1023:
                message = client.recv(1024)
                msg += message

            # broadcast(message)
            forward_to_receivers(message)

        else:
            # if no such message is recieved
            # we terminate the client and
            # broadcast that the client has
            # left the chat
            index = clients.index(client)
            nickname = nicknames[index]
            broadcast(flatten(dummyFIPA("client_disconnected",nickname)))
            print(f"{nickname} got disconnected")
            nicknames.remove(nickname)
            clients.remove(client)
            client.close()
            break

def recieve():

    while True:
        client, address = server.accept()
        # printing on the server the
        # notification of new connection
        print(f"connected with {str(address)}")

        # getting the nickname from the client
        # by sending them the codeword NICK

        client.send(flatten(dummyFIPA("server_topics", 'NICK')))
        nickname = unflatten(client.recv(1024)).content


        # adding nickname and client of the
        # client in the list

        nicknames.append(nickname)
        clients.append(client)
        client.send(flatten(dummyFIPA("active_agents", nicknames)))

        # printing nickname on server and broadcasting
        # the nickname to all clients in chat
        print(f" name of the client is {nickname}")
        broadcast(flatten(dummyFIPA("client_connected", nickname)))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("server is listening...")
recieve()