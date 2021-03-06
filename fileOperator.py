
BLOCK_SIZE = 3 #3 byte per block


class FileOperator:
    def __init__(self, filename):
        self.openFile(filename)

    def openFile(self, filename):
        self.file = open(filename, "rb")
        self.data = self.file.read()



    def getSize(self):
        return len(self.data) // BLOCK_SIZE

    def getBlock(self, blockNum):
        block = []
        for i in range(BLOCK_SIZE):
            block.append(self.data[blockNum * BLOCK_SIZE])
        return block

    def clear(self):
        self.file.close()
        self.data = None


    def getFile(self, data, name):
        self.file = open(name, "wb")
        for i in data:
            self.file.write(i)
        self.file.close()
        
def getDataBlock(filename, blocknumber):
    result = []
    file = open(filename, 'rb')
    data = file.read()

    if len(data) // BLOCK_SIZE < blocknumber:
        return None
    for i in range(BLOCK_SIZE):
        dataIndex = BLOCK_SIZE*blocknumber + i
        if dataIndex < len(data):
            result.append(data[dataIndex])
    return result

#blockData = getDataBlock("hehe.mp4", 1)


