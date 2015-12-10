import random

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.p = None
        self.disc = -1

    def __repr__(self):
        return "< %s %s %s >" % (self.key,self.p, self.disc)

    def __str__(self):
        return "< %s %s %s >" % (self.key,self.p, self.disc)

class BinaryTree:
    def __init__(self):
        self.root = None

    def length(self):
        return self.size

    def inorder(self, node):
        if node == None:
            return None
        else:
            self.inorder(node.left)
            print '(' + str(node.key[0]) + ', ' + str(node.key[1]) + ', ' + str(node.disc) + ')',
            self.inorder(node.right)

    def search(self, k):
        node = self.root
        node.disc = 0
        level = 0
        while node != None:
            if node.key == k:
                print "Level of searched node is(0 = root): " + str(level)
                return node
            level += 1
            if node.key[node.disc] > k[node.disc]:
                print str(k[node.disc]) + ' < ' + str(node.key[node.disc])
                node = node.left
            else:
                print str(k[node.disc]) + ' >= ' + str(node.key[node.disc])
                node = node.right
            node.disc = (node.disc +1) %2
        return None

    def minimum(self, node):
        x = None
        while node.left != None:
            x = node.left
            node = node.left
        return x

    def maximum(self, node):
        x = None
        while node.right != None:
            x = node.right
            node = node.right
        return x

    def successor(self, node):
        parent = None
        if node.right != None:
            return self.minimum(node.right)
        parent = node.p
        while parent != None and node == parent.right:
            node = parent
            parent = parent.p
        return parent

    def predecessor(self, node):
        parent = None
        if node.left != None:
            return self.maximum(node.left)
        parent = node.p
        while parent != None and node == parent.left:
            node = parent
            parent = parent.p
        return parent

    def insert(self, k):
        t = TreeNode(k)
        parent = None
        node = self.root
        while node != None:
            parent = node
            t.disc = (t.disc +1) %2
            if node.key[t.disc] > t.key[t.disc]:
                node = node.left
            else:
                node = node.right
        t.p = parent
        if parent == None:
            t.disc = 0
            self.root = t
        elif t.key[t.disc] < parent.key[t.disc]:
            parent.left = t
        else:
            parent.right = t
        return t


    def delete(self, node):
        if node.left == None:
            self.transplant(node, node.right)
        elif node.right == None:
            self.transplant(node, node.left)
        else:
            succ = self.minimum(node.right)
            if succ.p != node:
                self.transplant(succ, succ.right)
                succ.right = node.right
                succ.right.p = succ
            self.transplant(node, succ)
            succ.left = node.left
            succ.left.p = succ

    def transplant(self, node, newnode):
        if node.p == None:
            self.root = newnode
        elif node == node.p.left:
            node.p.left = newnode
        else:
            node.p.right = newnode
        if newnode != None:
            newnode.p = node.p
    def GetRoot(self):
        return self.root
if __name__ == "__main__":

    fout = open('output.txt', 'w')
    B = BinaryTree();
    data = ()
    for i in range(100):
        data = (random.randint(1,100),random.randint(1,100))
        B.insert(data)

    for i in range(9):
        data = (11*i,11*i)
        B.insert(data)
    B.insert((100,100))

    print B.inorder(B.GetRoot())
    print B.GetRoot()
    print (B.search((100,100)))


    fout.close()
    """If I wanted to insert pairs of numbers"""
    """
    for i in range(10):
        for j in range(10):
            r1 = random.randint(1,100)
            r2 = random.randint(1,100)
            B.insert([r1,r2])
            print (r1,r2)
   """
