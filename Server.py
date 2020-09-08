import socket
from datetime import datetime
"""
from PIL import ImageGrab
import base64

im = ImageGrab.grab()
im.save(r'C:\Sockets\screen.jpg')
file_name = 'C:\Sockets\screen.jpg'
"""
host = '127.0.0.1'  # 0.0.0.0
port = 8820
server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(10)

print "Server Started!"
print "Waiting for clients..."

(client_socket, client_address) = server_socket.accept()
client_socket.send("Welcome!")

client_user = client_socket.recv(1024)  # receive username
print client_user + " has connected!"

client_msg = client_socket.recv(1024)  # receive message
while True:
    if client_msg == "quit":
        print client_user + " has disconnected!"
        break

    time = str(datetime.now().hour) + ":" + str(datetime.now().minute)
    data = time + " " + client_user + " >> " + client_msg
    client_socket.send(data)
"""
    image = open(file_name, 'rb')
    file = base64.encode(image, basestring)
    client_socket.send(file)
"""
    client_msg = client_socket.recv(1024)  # receive message

client_socket.close()

server_socket.close()
