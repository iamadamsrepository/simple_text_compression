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
        # First convert file into string of bits using the tree
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
        length = 0
        for i in self.tree.treeList:
            if len(i[1]) > 15:
                length += 5
            else:
                length += 3
        byteArray = bytearray()
        byteArray += bytearray(iter([int(length / 256), length % 256]))
        for i in self.tree.treeList:
            byteArray += self.byteArrayFromKeyCharPair(i)
        self.treeByteArray = byteArray

    def byteArrayFromKeyCharPair(self, pair):
        char = pair[0]
        key = pair[1]

        if len(key) > 14:
            firstbit = '1'
            buffer = '1'
            while len(firstbit + buffer + key) < 32:
                buffer = '0' + buffer
        else:
            firstbit = '0'
            buffer = '1'
            while len(firstbit + buffer + key) < 16:
                buffer = '0' + buffer
        byteKey = firstbit + buffer + key

        byteArray = bytearray(iter([ord(char)]))
        for i in range(0, len(byteKey), 8):
            b = 0
            for val, pos in zip(byteKey[i:i+8], range(7,-1,-1)):
                if val == '1':
                    b += 1 << pos
            byteArray += bytearray(iter([b]))
        return byteArray

    def writeToFile(self):
        with open(self.fileOriginal[:-4] + ".compressed", "wb") as f:
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
        treeLength = list[0]*256 + list[1]
        self.treeList = []
        self.getTreeList(list[2: 2 + treeLength])
        # Decompress text
        self.text = ''
        self.getText(list[2 + treeLength:])
        # Write to file
        self.writeToFile()

    def getTreeList(self, treeArray):
        treeList = []
        nexti = 0
        while(nexti + 1< len(treeArray)):
            i = nexti
            char = chr(treeArray[i])
            if treeArray[i + 1] & (1<<7) > 0:
                keylength = 4
            else:
                keylength = 2
            nexti += keylength + 1
            key = self.getKey(treeArray[i+1: i+1+keylength])
            treeList.append((char, key))
        self.treeList = treeList

    def getKey(self, keycode):
        stringKey = ''
        start = 0
        for i in keycode:
            for j in range(8):
                if start == 1:
                    stringKey += str(int(i & (1 << (7-j)) > 0))
                if (i & (1 << (7-j))) > 0:
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
        if sys.argv[2][-4:] != '.txt':
            print('Compress .txt files only')
            exit()
        print(f"Compressing {sys.argv[2]}")
        Compress(sys.argv[2])
        print("Done.")

    elif sys.argv[1] == 'd':
        if sys.argv[2][-11:] != '.compressed':
            print("Decompress .compressed files only")
            exit()
        print(f"Decompressing {sys.argv[2]}")
        Decompress(sys.argv[2])
        print("Done.")

    else:
        printUsage()
    exit()