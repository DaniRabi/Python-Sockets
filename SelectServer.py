import socket
import select
from datetime import datetime

host = '127.0.0.1'  # 0.0.0.0
port = 8820
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(10)

print "Server Started!"
open_client_sockets = []
print "Waiting for clients..."

usernames = {}
messages_to_send = []

def send_waiting_messages(wlist):
    for message in messages_to_send:
        (client_socket, data) = message
        if (client_socket in wlist):
            client_socket.send(data)
        messages_to_send.remove(message)

while True:
    read_lst, write_lst, error_lst = select.select([server_socket] + open_client_sockets, open_client_sockets, [])

    time = str(datetime.now().hour) + ":" + str(datetime.now().minute)

    for current_socket in read_lst:
        if current_socket is server_socket:  # new client
            (client, address) = server_socket.accept()

            client.send("Welcome!")
            open_client_sockets.append(client)

            client_user = client.recv(1024)  # receive username

            print time + " " + client_user + " has connected!"

            # usernames.keys().append(current_socket)
            # usernames[current_socket] = str(client_user)
        else:
            # user = usernames[current_socket]
            user = "Username"

            client_msg = current_socket.recv(1024)  # receive message
            if client_msg == "quit":
                open_client_sockets.remove(current_socket)
                print time + " " + user + " has disconnected!"

                del usernames[current_socket]
            else:
                time = str(datetime.now().hour) + ":" + str(datetime.now().minute)
                data = time + " " + user + " >> " + client_msg + "\n"
                messages_to_send.append((current_socket, data))
    send_waiting_messages(write_lst)

server_socket.close()

# (0),(1),(2),(3) = username problem has to be solved