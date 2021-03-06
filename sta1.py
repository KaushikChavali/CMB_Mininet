import socket
import util
import sys
import time
import multiprocessing

readline = sys.stdin.readline

class globals:
    def __init__(self):
        self.fileBlockReceived = [False]
        self.fileBlocks = [0]

wifiConnected = False
fileLength = 0

def ReceiveHeartbeat(LocalIP, LocalPort, RemoteIP, RemotePort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LocalPort))
    sock.settimeout(10)
    
    # PROBLEM
    global wifiConnected

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data.startswith("HeartBeat"):
                #print "HeartBeat Received"
                wifiConnected = True
            else:
                print data
        except socket.timeout:
            #print "Receive Heartheat timeout"
            wifiConnected = False

def SendHeartbeat(LocalIP, LocalPort, RemoteIP, RemotePort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sock.bind((LocalIP, LocalPort))

    while True:
        sock.sendto("HeartBeat", (RemoteIP, RemotePort))
        time.sleep(4)

def ReceiveFileChunks(sockR, sockS, myGlobals):
    # PROBLEM: Variables NOT SYNCHRONIZED BETWEEN THREADS
    #global fileBlockReceived
    #global fileBlocks 
    
    while True:
        if sum(myGlobals.fileBlockReceived) >= fileLength:
            break
        print "blockCount:", sum(myGlobals.fileBlockReceived), " fileLength:", fileLength # Temporary
        try:
            data, addr = sockR.recvfrom(1024)
        except socket.timeout:
            continue
        seqNum = int(data.split(" ")[0]) # Temporary

        # Send ACK
        #sockS.sendto("Ack " + str(seqNum), (addr[0], addr[1])) # RemoteIP, RemotePort
        
        myGlobals.fileBlocks[seqNum] = data.split(" ")[1:] #Temporary
        #print "Received ", fileBlocks[seqNum] # Temporary
        myGlobals.fileBlockReceived[seqNum] = True
 
if __name__ == '__main__':

    # UDP Socket Send
    RemoteIPH = "10.1.0.3" # High bandwidth
    RemoteIP = "10.0.0.3" # Low bandwidth
    
    LocalIPH = "10.1.0.2" # High bandwidth
    LocalIP = "10.0.0.2" # Low bandwidth
    
    SendPort = 5005
    ReceivePort = 5006
    
    sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sockS.bind((LocalIP, SendPort))
    
    sockSH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sockSH.bind((LocalIPH, SendPort))
    
    sockR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sockR.bind((LocalIP, ReceivePort))
    sockR.settimeout(1)
    
    sockRH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # INTERNET, UDP
    sockRH.bind((LocalIPH, ReceivePort))
    sockRH.settimeout(1)
    
    myGlobals = globals()
    wifiConnected = False
    
    # Start Heartbeat
    p1 = multiprocessing.Process(target=SendHeartbeat, args=(LocalIPH, 5010, RemoteIPH, 5009))
    p1.start()
    p2 = multiprocessing.Process(target=ReceiveHeartbeat, args=(LocalIPH, 5009, RemoteIPH, 5010))
    p2.start()

    while True:
        print "Input request filename:",
        fileName = readline()
        #util.RecvACK(sock) 
        
        fileLength = 0
        while True:
            sockS.sendto(fileName, (RemoteIP, ReceivePort))
            #data, addr = sockR.recvfrom(1024)
            try:
                data, addr = sockR.recvfrom(1024)
            except socket.timeout:
                continue
            if data.startswith("Ack"):
                fileLength = int(data.split(" ")[1])
                print "Ack received, fileLength: ", fileLength
                break
            else:
                print data
        
        myGlobals.fileBlockReceived = [False]*fileLength
        myGlobals.fileBlocks = [0]*fileLength
        
        print "Receiving file..."

        t1 = time.time()
    
        #p3 = multiprocessing.Process(target=ReceiveFileChunks, args=(sockR, sockS, fileBlockReceived, fileBlocks))
        p3 = multiprocessing.Process(target=ReceiveFileChunks, args=(sockR, sockS, myGlobals))
        p3.start()
        
        #p4 = multiprocessing.Process(target=ReceiveFileChunks, args=(sockRH, sockSH, fileBlockReceived, fileBlocks))
        p4 = multiprocessing.Process(target=ReceiveFileChunks, args=(sockRH, sockSH, myGlobals))
        p4.start()
        
        p3.join()
        p4.join()

        delta = time.time() - t1
        print "Receive completed!"
        print "Time elapsed:", delta
        print "Speed: ", fileLength/delta, "Blocks/second"


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
