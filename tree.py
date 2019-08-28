class TreeMaker:
    def __init__(self, file):
        # Read file and count characters
        table = getTable(file)
        # Create priority queue from table
        queue = getQueue(table)
        # Create a character tree
        self.tree = Node("")
        self.makeTree(queue)
        # Make a list of tree values
        self.treeList = []
        self.writeTree(self.tree, "")
        self.treeSort()

    def makeTree(self, queue):
        # Until the whole queue becomes one tree
        while queue.__len__() > 1:
            # Pop 2 Tuples, calculate weight, join into combined node
            t1 = queue.pop()
            t2 = queue.pop()
            w = t1[1] + t2[1]
            if isinstance(t1[0], Node):
                n1 = t1[0]
            else:
                n1 = Node(t1[0])
            if isinstance(t2[0], Node):
                n2 = t2[0]
            else:
                n2 = Node(t2[0])
            n = Node("")
            n.left = n1
            n.right = n2
            # Put new node into queue
            insertQueue(queue, (n, w))
        # Return the tree
        self.tree = queue[0][0]

    def writeTree(self, node, str):
        # If character found, list the character and bit string
        if node.data != "":
            self.treeList.append((node.data, str))
        # Recursive over children
        if node.left is not None:
            self.writeTree(node.left, str + "0")
        if node.right is not None:
            self.writeTree(node.right, str + "1")

    def treeSort(self):
        self.treeList.sort(key=lambda x: 10000 * len(x[1]) + int(x[1], 2))

    def __str__(self):
        string = ""
        for i in self.treeList:
            string += f"{i[0]}: {i[1]}\n"
        return string


def getTable(file):
    # Initialise table
    table = []
    for i in range(256):
        table.append(0)
    # Count characters in file
    fp = open(file, 'r')
    for i in fp.read():
        if ord(i) < 256:
            table[ord(i)] += 1
        else:
            print(f"Error: {i} not in range")
    fp.close()
    return table


def getQueue(table):
    queue = []
    count = 0
    for i in table:
        if i > 0:
            queue.append((chr(count), i))
        count += 1
    queue.sort(reverse=True, key=lambda t: t[1])
    return queue


def insertQueue(queue, tuple):
    queue.append(tuple)
    queue.sort(reverse=True, key=lambda t: t[1])


def makeTree(queue):
    # Until the whole queue becomes one tree
    while queue.__len__() > 1:
        # Pop 2 Tuples, calculate weight, join into combined node
        t1 = queue.pop()
        t2 = queue.pop()
        w = t1[1] + t2[1]
        if isinstance(t1[0], Node):
            n1 = t1[0]
        else:
            n1 = Node(t1[0])
        if isinstance(t2[0], Node):
            n2 = t2[0]
        else:
            n2 = Node(t2[0])
        n = Node("")
        n.left = n1
        n.right = n2
        # Put new node into queue
        insertQueue(queue, (n, w))
    # Return the tree
    return queue[0][0]


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
