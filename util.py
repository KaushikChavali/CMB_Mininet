import multiprocessing

import random #temporary

def RecvACKprocess(sock):
    while True:
        data, addr = sock.recvfrom(1024)
        if data == "Ack":
            print("Ack received")
            break
def RecvACK(sock):
    p = multiprocessing.Process(target=RecvACKprocess, args=(sock,))
    p.start()
    p.join(1)
    # If process is still active, we kill it
    if p.is_alive():
      p.terminate()
      p.join()    

def getFileChunks(fileName, chunkSize = 1000):
    # TODO openfile and return chunks of file


    '''
    version 1
    result = []
    file = open(fileName, 'rb')
    data = file.read()
    for i in range(0,chunkSize,3):
        temp = []
        j = 0
        while i+j < len(data) or j == 3:
            temp.append(data[i+j])
        result.append(temp)
    return result
    '''
    print('file name: ' + fileName[:-1]) #remove \n
    file = open(fileName[:-1], 'rb')
    data = file.read()
    file.close()
    return data

def saveFileFromChunks(blocksOfFile, fileName):
    print(getFileChunks(fileName))
    newname = fileName.split('.')[0] + ' copy.' + fileName.split('.')[1]
    file = open(newname, 'wb')
    print("--------------------------------------------------------------")
    print(blocksOfFile)
    for i in blocksOfFile:
        file.write(i[0])
    file.close()

def toByte(data):
    return data.encode('utf-8')

def toString(data):
    return data.decode('utf-8')

def getPacket(isAck, seqNumber, data = None):
    if isAck:
        return bytes(0) + bytes(seqNumber)
    else:
        return bytes(1) + bytes(seqNumber) + data

def getValueFromPacket(packet):
    data = packet[-1]
    if int(packet[0]) == 1:
        #isNotAck
        return (False, int(packet[1:-1]), packet[-1])
    else:
        return (True, packet[0], int(packet[1:]))




class Packet:
    def __init__(self, seq, ack, isSyn, isAck):
        self.seq = seq
        self.ack = ack
        self.isSyn = isSyn
        self.isAck = isAck
