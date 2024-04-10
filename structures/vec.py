class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)
    
    __iadd__ = __add__

    def __mul__(self, other):
        return vec2(self.x * other, self.y * other)
    
    __rmul__ = __mul__

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y