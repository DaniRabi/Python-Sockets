import socket
from datetime import datetime
from thread import *

host = '192.168.140.29'
port = 8820
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(10)

print "Server Started!"
print "Waiting for clients..."

open_client_sockets = []
messages_to_send = []

def send_pending_messages():
    while True:
        if len(messages_to_send) > 0:
            for message in messages_to_send:
                for client in open_client_sockets:
                    client.send(message)
                messages_to_send.remove(message)


def  clientthread(conn):
    conn.send("Welcome!")
    open_client_sockets.append(conn)

    time = str(datetime.now().hour) + ":" + str(datetime.now().minute)

    client_user = conn.recv(1024)  # receive username

    prefix = time + " " + client_user
    connect_msg = prefix + " has connected!"
    print connect_msg

    client_msg = ""
    data = connect_msg
    while client_msg != "quit":
        messages_to_send.append(data)

        time = str(datetime.now().hour) + ":" + str(datetime.now().minute)

        client_msg = conn.recv(1024)  # receive message
        prefix = time + " " + client_user
        data = prefix + " >> " + client_msg + "\n"

    open_client_sockets.remove(conn)

    disconnect_msg = prefix + " has disconnected!"
    print disconnect_msg
    messages_to_send.append(disconnect_msg)
    conn.close()


start_new_thread(send_pending_messages, ())
while True:
    (client_socket, client_address) = server_socket.accept()

    start_new_thread(clientthread ,(client_socket,))

server_socket.close()