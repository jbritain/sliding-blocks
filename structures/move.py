class Move:
    def __init__(self, old_pos, movement):
        self.old_pos = old_pos
        self.movement = movement
        self.new_pos = old_pos + movement

    def __str__(self):
        return f"{self.old_pos.y} {self.old_pos.x} {self.new_pos.y} {self.new_pos.x}"