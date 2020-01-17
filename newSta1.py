import socket
import threading
import time
import sys

#how to use: 
#app = FTP()
#app.run()

class FTP:
    def __init__(self):

        #global here
        self.fileBlockReceived = [False]
        self.fileBlocks = [0]
        self.wifiConnected = False
        self.fileLength = 0

        self.remoteIPH = "10.1.0.3"
        self.remoteIP = "10.0.0.3"

        self.localIPH = "10.1.0.2"
        self.localIP = "10.0.0.2"

        self.sendPort = 5005
        self.recvPort = 5006
        self.recvAckPort = 5007

        self.initSocket()
        self.initHeartBeat()

    def initSocket(self):
        self.sockS = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockS.bind((self.localIP, self.sendPort))

        self.sockSH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockSH.bind((self.localIPH, self.sendPort))

        self.sockR = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockR.bind((self.localIP, self.recvPort))
        self.sockR.settimeout(1)

        self.sockRH = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockRH.bind((self.localIPH, self.recvPort))
        self.sockRH.settimeout(0.5)

    def initHeartBeat(self):
        self.sendHeartBeatThread = threading.Thread(target=self.sendHeartbeat)
        self.recvHeartBeatThread = threading.Thread(target=self.receiveHeartbeat)
        self.sendHeartBeatThread.start()
        self.recvHeartBeatThread.start()

    def run(self):
        while True:
            print "Input request filename:",
            fileName = sys.stdin.readline()
            self.fileLength = 0
            while True:
                self.sockS.sendto(fileName, (self.remoteIP, self.recvPort))
                try:
                    data,addr = self.sockR.recvfrom(1024)
                except socket.timeout:
                    continue
                if data.startswith("Ack"):
                    self.fileLength = int(data.split(" ")[1])
                    print("Ack received, fileLength: " + str(self.fileLength))
                    break
                else:
                    print(data)
            self.fileBlockReceived = [False] * self.fileLength
            self.fileBlocks = [0] * self.fileLength
            print("recving file")

            t1 = time.time()

            lowChunkThread = threading.Thread(target=self.receiveFileChunks, args=(self.sockR, self.sockS, False))
            highChunkThread = threading.Thread(target=self.receiveFileChunks, args=(self.sockRH, self.sockSH, True))
            lowChunkThread.start()
            highChunkThread.start()

            lowChunkThread.join()
            highChunkThread.join()

            delta = time.time() - t1
            print("recv completed!")
            print("time elapsed: ", delta)
            print("speed: " + str(self.fileLength / delta) + "Blocks/second")
    
    def receiveFileChunks(self, receiver, sender, isHighSpeed):
        while sum(self.fileBlockReceived) < self.fileLength:
            #print "blockCount:", sum(self.fileBlockReceived), " fileLength:", self.fileLength  # Temporary
            try:
                data, addr = receiver.recvfrom(1024)
            except socket.timeout:
                continue
            seqNum = int(data.split(" ")[0])  # Temporary

            # Send ACK
            if isHighSpeed:
                print "Received through Wifi ", str(seqNum)
                sender.sendto("Ack " + str(seqNum), (self.remoteIPH, self.recvAckPort))
            else:
                sender.sendto("Ack " + str(seqNum), (self.remoteIP, self.recvAckPort))

            self.fileBlocks[seqNum] = data.split(" ")[1:]  # Temporary
            self.fileBlockReceived[seqNum] = True


    def sendHeartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET, UDP
        sock.bind((self.localIP, 5010))

        while True:
            sock.sendto("HeartBeat", (self.remoteIP, 5009))
            time.sleep(4)

    def receiveHeartbeat(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET, UDP
        sock.bind((self.localIP, 5009))
        sock.settimeout(10)

        if self.wifiConnected:
            print("HURAYYYYYYYYYYYYYYYYYYYY")

        while True:
            try:
                data, addr = sock.recvfrom(1024)
                if data.startswith("HeartBeat"):
                    # print "HeartBeat Received"
                    wifiConnected = True
                else:
                    print data
            except socket.timeout:
                # print "Receive Heartheat timeout"
                wifiConnected = False


if __name__ == '__main__':

    app = FTP()
    app.run()
