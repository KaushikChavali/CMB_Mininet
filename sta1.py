# This file contains some possibility in implementation
# UDP Socket is preferred

# UDP Socket Send
import socket
 
UDP_IP = "10.0.0.3"
UDP_PORT = 5005
MESSAGE = "Hello, World!"
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

#UDP Socket Receive

#import socket
#
#UDP_IP = "10.0.0.2"
#UDP_PORT = 5005
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
#sock.bind((UDP_IP, UDP_PORT))
#
#while True:
#    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#    print "received message:", data