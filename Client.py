import socket
from thread import *

my_socket = socket.socket()
my_socket.connect(('192.168.140.29', 8820))

msg = my_socket.recv(1024)
print msg

user = raw_input("Write Username: ")
my_socket.send(user)

def send_messages():
    message = ""
    while message != "quit":
        message = raw_input()
        my_socket.send(message)
    my_socket.close()

start_new_thread(send_messages, ())

while True:
    try:
        updates = my_socket.recv(2014)
    except socket.error:
        break
    print updates