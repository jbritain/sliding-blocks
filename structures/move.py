class Move:
    def __init__(self, old_pos, new_pos):
        self.old_pos = old_pos
        self.new_pos = new_pos

    def __str__(self):
        return f"{self.old_pos.y} {self.old_pos.x} {self.new_pos.y} {self.new_pos.x}"