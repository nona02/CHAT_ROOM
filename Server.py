import socket
import threading

port=50000
host=socket.gethostbyname(socket.gethostname())

address=(host,port)
format="utf-8"
clients=[]
names=[]
#create a new socket for thr server where AF_INET is the type of Address(will return IPv4) and SOCK_STREAM is the TCP socket
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind(address)

def startchat():
    print("Server is working on " + host)
    server.listen()
    while True:
        connection,add=server.accept()
        connection.send("NAME".encode(format))
        name=connection.recv(1025).decode(format)
        names.append(name)
        clients.append(connection)
        print(f"Name is : {name}")
        #print(f"Client is:{connection}")
        broadcastMessage(f"{name} has joined the group".encode(format))
        connection.send("Connection successful".encode(format))
        thread= threading.Thread(target=receive,args=(connection,add))
        thread.start()
        print(f"active connections {threading.active_count()-1}")

def receive(connection,add):
    print(f"New Connection : {add}")
    connected=True

    while connected:
        message=connection.recv(1025)
        broadcastMessage(message)

    connection.close()


def broadcastMessage(message):
    for client in clients:
        client.send(message)

startchat()