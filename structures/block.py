from .vec import vec2
from .move import Move

def taxicab_distance(pos_1, pos_2):
	return abs(pos_1.x - pos_2.x) + abs(pos_1.y - pos_2.y)

def all_ones(n):
    return ((n+1) & n == 0) and (n!=0)

class Block:
    row_sums = {}
    col_sums = {}

    def __init__(self, length, width, y, x):
        self.position = vec2(x, y)
        self.size = vec2(width, length)
        self.available_moves = None
        self.goal_distance_val = None
    

    @property
    def height(self):
        return self.size.y
    
    @property
    def width(self):
        return self.size.x

    def generate_available_moves(self, board):
        

        moves = []

        # ===Horizontal Moves===

        occupied_hor = board.get_occupied(False)[self.position.y:self.position.y + self.size.y]

        sum_hor = 0
        #print("rows:")
        for row in occupied_hor:
            #print("    " + bin(row))
            sum_hor |= row

        past_hor_moves = Block.row_sums.get((self.position.x, self.size.x, self.size.x, sum_hor))
        
        if past_hor_moves:
           #print(f"  Horizontal cache hit: {self.position.x}, {self.size.x}, {bin(sum_hor)}")
            moves.extend(map(lambda m: Move(self.position, m), past_hor_moves)) # create move from the movement
        else:
            horizontal_moves = []
            if not (all_ones(sum_hor) and sum_hor.bit_length == board.width):
                #print(f"row sum: {bin(sum_hor)}")
                right_width = board.width - (self.position.x + self.size.x) # spaces to the right of our block
                right = sum_hor & ((1 << right_width) - 1) # keep only bits to the right of the block
                left = sum_hor >> board.size.x - (self.position.x) # keep only bits to the left of the block

                #print(f"left: {bin(left)}")
                #print(f"right: {bin(right)}")

                if left == 0: # nothing to the left of us
                    left_distance = self.position.x
                else:
                    left_distance = max(0, (left & -left).bit_length() - 1) # how far left can we move
                #print("left distance:", left_distance)

                for x in range(left_distance):
                    horizontal_moves.append(Move(self.position, vec2(-(x + 1), 0)))
                
                right_distance = right_width - right.bit_length() if right_width != 0 else 0 # if we are on the right just return 0 because we get 1 when we shouldn't
                #print("right distance: ", right_distance)

                for x in range(right_distance):
                    horizontal_moves.append(Move(self.position, vec2(x+1, 0)))
            else:
                print("all ones hor") 
            moves += horizontal_moves 
            Block.row_sums[(self.position.x, self.size.x, sum_hor)] = list(map(lambda m: m.movement, horizontal_moves)) # only store movement since the block that has the move might be a different one
           #print(f"  Horizontal cache write: {self.position.x}, {self.size.x}, {bin(sum_hor)}")

        # ===vertical Moves===

        occupied_ver = board.get_occupied(True)[self.position.x:self.position.x + self.size.x]
        
        sum_ver = 0
        #print("cols")
        for col in occupied_ver:
            #print("    " + bin(col))
            sum_ver |= col

        past_ver_moves = Block.col_sums.get((self.position.y, self.size.y, sum_ver))
        if past_ver_moves:
            

           #print(f"  Vertical cache hit: {self.position.y}, {self.size.y}, {bin(sum_ver)}")
            moves.extend(map(lambda m: Move(self.position, m), past_ver_moves))
            if f"{self.position.y}, {self.size.y}, {bin(sum_ver)}" == "0, 2, 0b1100":
                pass
        else:
            vertical_moves = []
            if not (all_ones(sum_ver) and sum_ver.bit_length == board.height):
                #print(f"col sum: {bin(sum_ver)}")
                bottom_height = board.height - (self.position.y + self.size.y) # spaces below our block
                bottom = sum_ver & ((1 << bottom_height) - 1) # keep only bits below the block
                top = sum_ver >> board.size.y - (self.position.y) # keep only bits above the block

                #print(f"bottom: {bin(bottom)}")
                #print(f"top: {bin(top)}")

                if top == 0: # nothing above us
                    top_distance = self.position.y
                else:
                    top_distance = max(0, (top & -top).bit_length() - 1) # how far up can we move
                #print("top distance:", top_distance)

                for y in range(top_distance):
                    vertical_moves.append(Move(self.position, vec2(0, -(y + 1))))

                
                bottom_distance = bottom_height - bottom.bit_length() if bottom_height != 0 else 0 # if we are on the right just return 0 because we get 1 when we shouldn't
                #print("bottom distance:", bottom_distance)

                for y in range(bottom_distance):
                    vertical_moves.append(Move(self.position, vec2(0, y+1)))
            else:
                print("all ones ver")   
            Block.col_sums[(self.position.y, self.size.y, sum_ver)] = list(map(lambda m: m.movement, vertical_moves))
            #print(f"  Vertical cache write: {self.position.y}, {self.size.y}, {bin(sum_ver)}")
            moves += vertical_moves

        return moves
    
    def get_available_moves(self, board):
        if self.available_moves is None:
            self.available_moves = self.generate_available_moves(board)
        return self.available_moves
    
    def generate_goal_distance(self, board):
        if board.big_tray:
            return 0
        distance = 0
        for goal in board.goals:
            if self.size != goal.size:
                next
            elif self.position == goal.position:
                return 0
            else:
                distance += taxicab_distance(self.position, goal.position)
        return distance

    def get_goal_distance(self, board):
        if self.goal_distance_val == None:
            self.goal_distance_val = self.generate_goal_distance(board)
        return self.goal_distance_val
    
    def __eq__(self, other):
        return self.position == other.position and self.size == other.size
    
    def __str__(self):
        return f"{self.size.y} {self.size.x} {self.position.y} {self.position.x}"

