class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        return self.stack.append(item)
    
    def pop(self):
        return self.stack.pop()
    
    def __len__(self):
        return len(self.stack)
    
    # note that this extends to the top of the stack.
    # the last element in ext will be at the top of the stack
    def extend(self, ext):
        return self.stack.extend(ext)