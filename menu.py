class node: 
    def __init__(self, entry, parent = None):
        self.entry = entry
        self.sibling = None
        self.leftChild = None
        self.parent = parent


class entry: 
    def __init__(self, title, description, directory, newid):
        self.title = title
        self.description = description
        self.directory = directory
        self.id = newid