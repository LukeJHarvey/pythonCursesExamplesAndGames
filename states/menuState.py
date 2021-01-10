from states.state import state
from menu import node, entry
import curses
import json
class menuState(state):
    def __init__(self):
        self.root = node(entry("Main", "", True, ''))
        self.currentDir = self.root
        self.num = 0
        self.size = 0
        with open('static/menuItems.json') as f:
            menuItems = json.load(f)
            self.createAllDirectories(menuItems)
        self.size = self.levelSize()
        pass

    def cleanUp(self):
        pass

    def pause(self):
        pass
    def resume(self):
        pass

    def handleEvents(self, manager):
        i = manager.scene.getch()
        if(i == curses.KEY_UP):
            self.num = (self.num - 1, self.size-1)[self.num - 1 < 0]
        elif(i == curses.KEY_DOWN):
            self.num = (self.num + 1, 0)[self.num + 1 >= self.size]
        elif(i == curses.KEY_RIGHT):
            if(self.currentDir.leftChild != None):
                x = self.getSibling(self.currentDir,self.num)
                if(x.entry.directory):
                    self.currentDir = self.getSibling(self.currentDir,self.num)
                    self.size = self.levelSize()
                    self.num = 0
                    manager.scene.clear()
                else:
                    manager.pushState(x.entry.id)
                    manager.scene.clear()
        elif(i == curses.KEY_LEFT and self.root != self.currentDir):
            self.currentDir = self.currentDir.parent
            self.size = self.levelSize()
            self.num = 0
            manager.scene.clear()
        elif(i == ord('q')):
            manager.scene.clear()
            manager.running = False

    def update(self, manager):
        pass
    def draw(self, manager):
        i = 0
        n = self.currentDir.leftChild
        while(n != None):
            attr = (curses.A_NORMAL, curses.A_STANDOUT)[self.num==i]
            manager.scene.addstr(i,0,n.entry.title, attr)
            i += 1
            n = n.sibling
        i += 1
        manager.scene.addstr(i,0,str(self.size), curses.A_STANDOUT)
        manager.scene.refresh()

    def createAllDirectories(self, menuItems):
        for item in menuItems['items']:
            newEntry = entry(item['title'], item['description'], item['directory'], item['id'])
            n_node = self.root
            if(item['parent'] == "Main"):
                if(n_node.leftChild == None):
                    n_node.leftChild = node(newEntry, self.root)
                else:
                    n_node = n_node.leftChild
                    while(n_node.sibling != None):
                        n_node = n_node.sibling
                    n_node.sibling = node(newEntry, self.root)
            else:
                n_node = self.DFSSearch(self.root, item["parent"])
                p_node = n_node
                if(n_node == None):
                    pass
                elif(n_node.leftChild != None):
                    n_node = n_node.leftChild
                    while(n_node.sibling != None):
                        addNode = addNode.sibling
                    n_node.sibling = node(newEntry, p_node)
                else:
                    n_node.leftChild = node(newEntry, p_node)
                    
    def DFSSearch(self, root, goal):
        if(root):
            print(root.entry.title)
            x = self.DFSSearch(root.leftChild, goal)
            y = self.DFSSearch(root.sibling, goal)
            if(root.entry.title == goal):
                return root
            elif(x):
                return x
            elif(y):
                return y
            
    def levelSize(self):
        n = self.currentDir.leftChild
        size = 0
        while(n != None):
            size += 1
            n = n.sibling
        return size

    def getSibling(self, root, num):
        n = root.leftChild
        while(n != None and num != 0):
            num -= 1
            n = n.sibling
        return n
