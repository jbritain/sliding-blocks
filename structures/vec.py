class vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)
    
    def __abs__(self):
        if self.x >= 0:
            x = self.x
        else:
            x = -self.x

        if self.y >= 0:
            y = self.y
        else:
            y = -self.y
        
        return vec2(x, y)
    
    __iadd__ = __add__

    def __mul__(self, other):
        return vec2(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        if other.x == 0 or self.x == 0:
            x = 0
        else:
            x = self.x / other.x

        if other.y == 0 or self.y == 0:
            y = 0
        else:
            y = self.y / other.y

        return vec2(x, y)
    
    __rmul__ = __mul__

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y