from .vec import vec2

class Block:
    def __init__(self, x, y, width, height):
        self.position = vec2(x, y)
        self.size = vec2(x, y)