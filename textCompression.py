import sys
from tree import TreeMaker


class Compress:
    def __init__(self, file):
        self.fileOriginal = file
        # Get the tree
        self.tree = TreeMaker(file)
        print(self.tree)
        # Compress file into byteArray
        self.fileByteArray = bytearray()
        self.compressFile()
        # Convert the tree key into byteArray
        self.treeByteArray = bytearray()
        self.compressTree()
        # Write the byteArrays to file
        self.writeToFile()

    def compressFile(self):
        # First convert file into string of 0s and 1s using the tree
        charString = ""
        f = open(self.fileOriginal, "r")
        for i in f.read():
            for j in self.tree.treeList:
                if i == j[0]:
                    charString += j[1]
        # Convert string into list of ints
        intList = []
        for i in range(len(charString) - 8, -8, -8):
            a = 0
            for j in range(8):
                a *= 2
                if i + j >= 0 and charString[i + j] == "1":
                    a += 1
            intList.insert(0, a)
        f.close()
        # The file contents start of the first 1 in the sequence
        if len(charString) % 8 == 0:
            intList.insert(0, 1)
        else:
            intList[0] = intList[0] | (1 << len(charString) % 8)
        self.fileByteArray = bytearray(iter(intList))

    def compressTree(self):
        byteArray = bytearray()
        byteArray += bytearray(iter([len(self.tree.treeList)]))
        for i in self.tree.treeList:
            byteArray += bytearray(iter([ord(i[0])]))
            b = 1
            for j in i[1]:
                b *= 2
                if j == '1':
                    b += 1
            byteArray += bytearray(iter([int((b - b % 256)/256), b % 256]))
        self.treeByteArray = byteArray

    def writeToFile(self):
        with open(self.fileOriginal + ".compressed", "wb") as f:
            f.write(self.treeByteArray)
            f.write(self.fileByteArray)
            f.close()


class Decompress:
    def __init__(self, file):
        with open(file, "rb") as f:
            # Read file into list of ints
            list = []
            byte = f.read(1)
            while byte:
                list.append(int.from_bytes(byte, byteorder='big'))
                byte = f.read(1)
            f.close()
        # Make tree list
        self.treeList = []
        self.getTreeList(list[1:list[0]*3 + 1])
        # Decompress text
        self.text = ''
        self.getText(list[list[0]*3 + 1:])
        # Write to file
        self.writeToFile()

    def getTreeList(self, treeArray):
        treeList = []
        for i in range(0, len(treeArray), 3):
            char = chr(treeArray[i])
            key = self.getKey(treeArray[i + 1], treeArray[i + 2])
            treeList.append((char, key))
        self.treeList = treeList

    def getKey(self, byte1, byte2):
        stringKey = ''
        start = 0
        for j in range(8):
            if start == 1:
                stringKey += str(int((byte1 & (1 << (7-j))) > 0))
            if byte1 & (1 << (7-j)):
                start = 1
        for j in range(8):
            if start == 1:
                stringKey += str(int((byte2 & (1 << (7-j))) > 0))
            if byte2 & (1 << (7-j)):
                start = 1
        return stringKey

    def getText(self, textArray):
        start = 0
        text = ''
        curr = ''
        for i in textArray:
            for j in range(7, -1, -1):
                bit = int((i & (1 << j)) > 0)
                if start == 1:
                    curr += str(bit)
                    for k in self.treeList:
                        if curr == k[1]:
                            text += k[0]
                            curr = ''
                            continue
                if bit == 1:
                    start = 1
        self.text = text

    def writeToFile(self):
        with open('decomp.txt', 'w') as f:
            f.write(self.text)
            f.close()


def printUsage():
    print("Usage: python3 textCompression.py [c or d] text")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        printUsage()

    elif sys.argv[1] == 'c':
        print(f"Compressing {sys.argv[2]}")
        Compress(sys.argv[2])
        print("Done.")

    elif sys.argv[1] == 'd':
        if sys.argv[2][-10:] != 'compressed':
            print("Decompress .compressed files only")
            exit()
        print(f"Decompressing {sys.argv[2]}")
        Decompress(sys.argv[2])
        print("Done.")

    else:
        printUsage()
    exit()
