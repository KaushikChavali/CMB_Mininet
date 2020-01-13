import socket
import util
import sys
import time
import multiprocessing

readline = sys.stdin.readline


def ReceiveHeartbeat(LocalIP, LocalPort, RemoteIP, RemotePort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LocalPort))
    sock.settimeout(10)

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data.startswith("HeartBeat"):
                print "HeartBeat Received"
                #global wifiConnected
                wifiConnected = True
            else:
                print data
        except socket.timeout:
            print "Receive Heartheat timeout"
            #global wifiConnected
            wifiConnected = False

def SendHeartbeat(LocalIP, LocalPort, RemoteIP, RemotePort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LocalPort))

    while True:
        sock.sendto("HeartBeat", (RemoteIP, RemotePort))
        time.sleep(4)
 
if __name__ == '__main__':

    # UDP Socket Send
    RemoteIPH = "10.1.0.3" # High bandwidth
    RemoteIP = "10.0.0.3" # Low bandwidth
    RemotePort = 5005
    
    LocalIPH = "10.1.0.2" # High bandwidth
    LocalIP = "10.0.0.2" # Low bandwidth
    LocalPort = 5005
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LocalPort))
    
    wifiConnected = False
    
    # Start Heartbeat
    p = multiprocessing.Process(target=SendHeartbeat, args=(LocalIPH, 5010, RemoteIPH, 5009))
    p.start()
    p = multiprocessing.Process(target=ReceiveHeartbeat, args=(LocalIPH, 5009, RemoteIPH, 5010))
    p.start()

    while True:
        print("Input request filename:"),
        fileName = readline()
        sock.sendto(fileName, (RemoteIP, RemotePort))
        #util.RecvACK(sock) 
        
        fileLength = 0
        while True:
            data, addr = sock.recvfrom(1024)
            if data.startswith("Ack"):
                fileLength = int(data.split(" ")[1])
                print "Ack received, fileLength: ", fileLength
                break
            else:
                print data
        
        fileBlockReceived = [False]*fileLength
        fileBlockReceivedCount = 0
        fileBlocks = [0]*fileLength
        
        # TODO Receive file
        print "Receiving file..."

        while fileBlockReceivedCount < fileLength:
            data, addr = sock.recvfrom(1024)
            seqNum = int(data.split(" ")[0]) # Temporary

            # Send ACK
            #sock.sendto("Ack " + str(seqNum), (addr[0], addr[1])) # RemoteIP, RemotePort
            
            fileBlocks[seqNum] = data.split(" ")[1:]
            print "Received ", fileBlocks[seqNum] # Temporary
            fileBlockReceived[seqNum] = True
            fileBlockReceivedCount += 1
        
        print "Receive completed!"


    #UDP Socket Receive
    #
    #UDP_IP = "10.1.0.2" # High bandwidth
    #UDP_IP = "10.0.0.2" # Low bandwidth
    #UDP_PORT = 5005
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    #sock.bind((UDP_IP, UDP_PORT))
    #
    #while True:
    #    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #    print "received message:", data
