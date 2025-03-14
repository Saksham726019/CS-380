import sys
import random
import time
from queue import PriorityQueue

class SlidingBrick:
    def __init__(self, w: int, h: int, board: list):
        self.__width: int = w
        self.__height: int = h
        self.__board: list = board
        self.__emptyCells: list = []
        self.__masterBrickPositions: list = []
        self.__exitPositions: list = []
        self.__move: tuple = None
        self.__parent: SlidingBrick = None
    
    # Function to set the parent.
    def setParent(self, parent) -> None:
        self.__parent = parent
    
    # Function to get the parent.
    def getParent(self):
        return self.__parent
    
    # Function to set the move that led to this current state.
    def setMove(self, move: tuple) -> None:
        self.__move = move
    
    # Function to get the move that led to this current state.
    def getStateMove(self) -> tuple:
        return self.__move

    # Function to get the height of the board.
    def getHeight(self) -> int:
        return self.__height
    
    # Function to get the width of the board.
    def getWidth(self,) -> int:
        return self.__width
    
    # Function to return the board.
    def getBoard(self) -> list:
        return self.__board
    
    # Function to print the board.
    def printBoard(self) -> None:
        print(f"{self.__width},{self.__height},")

        # Print each row of the board
        for row in self.__board:
            items: str = ""

            for item in row:
                items += str(item) + ", "
            
            print(f" {items}")
    
    # Function to copy and return the initial (original) board.
    def cloneBoard(self) -> list:
        cloned_board: list = []

        for row in self.__board:
            cloned_board.append(row[:])

        return cloned_board
    
    # Function to check if we have reached the goal state.
    def isGoalState(self) -> bool:
        for row in self.__board:
            if -1 in row:
                return False
                    
        return True
    
    # Function to update the empty cells location.
    def updateEmptyCells(self, prev_positions: list, new_positions: list) -> None:
        for position in prev_positions:
            if position in self.__emptyCells:
                self.__emptyCells.remove(position)
            
        self.__emptyCells.extend(new_positions)

    # Function to find empty cells (0) in the board.
    def findEmptyCells(self) -> None:
        self.__emptyCells.clear()
        for h in range(self.__height):
            for w in range(self.__width):
                if self.__board[h][w] == 0:
                    self.__emptyCells.append((h, w))
    
    # Function to return the empty cells location.
    def getEmptyCells(self) -> list:
        return self.__emptyCells
    
    # Function to set the empty cells/
    def setEmptyCells(self, emptyCells: list) -> None:
        self.__emptyCells = emptyCells.copy()
    
    # Function to find the exit positions.
    def findExitPositions(self) -> None:
        self.__exitPositions.clear()
        for h in range(self.__height):
            for w in range(self.__width):
                if self.__board[h][w] == -1:
                    self.__exitPositions.append((h, w))
    
    # Function to get the exit positions.
    def getExitPositions(self) -> list:
        return self.__exitPositions
    
    # Function to set the exit positions.
    def setExitPositions(self, exitPositions: list) -> None:
        self.__exitPositions = exitPositions.copy()

    # Function to find the master brick (2) in the board.
    def findMasterBrick(self) -> None:
        self.__masterBrickPositions.clear()
        for h in range(self.__height):
            for w in range(self.__width):
                if self.__board[h][w] == 2:
                    self.__masterBrickPositions.append((h, w))
    
    # Functon to return master brick locations in the board.
    def getMasterBrickPositions(self) -> list:
        self.findMasterBrick()
        return self.__masterBrickPositions

    # Function to check if adjacent cells are the same valued bricks.
    def checkAdjacent(self, h: int, w: int, brick: int) -> set:
        adjacent = set()
        for i in range(self.__height):
            for j in range(self.__width):
                if (i, j) != (h, w) and self.__board[i][j] == brick:        # Add the locations of the brick except the starting ones.
                    adjacent.add((i, j))

        return adjacent

    # Function to get the moves of masterbrick towards the exit (-1) if there is any.
    def masterBrickMovesToExit(self) -> set:
        moves: set = set()

        # If -1 is on top of the board.
        top_exits = [(row, column) for (row, column) in self.__exitPositions if row == 0]

        # If -1 is on bottom of the board.
        bottom_exits = [(row, column) for (row, column) in self.__exitPositions if row == self.__height - 1]

        # If -1 is on the left side of the board.
        left_exits = [(row, column) for (row, column) in self.__exitPositions if column == 0]

        # If -1 is on the right side of the board.
        right_exits = [(row, column) for (row, column) in self.__exitPositions if column == self.__width - 1]

        # If the cell below is 2 for each exit position, then the move (2, up) is valid.
        if top_exits:
            valid = True
            for (row, column) in top_exits:
                # Check that the cell below exists and is brick 2.
                if self.__board[row + 1][column] != 2:
                    valid = False
                    break
            if valid:
                moves.add((2, "up"))

        # If the cell above is 2 for each exit position, then the move (2, down) is valid.
        elif bottom_exits:
            valid = True
            for (row, column) in bottom_exits:
                if self.__board[row - 1][column] != 2:
                    valid = False
                    break
            if valid:
                moves.add((2, "down"))

        # If the cell on right is 2 for each exit position, then the move (2, left) is valid.
        elif left_exits:
            valid = True
            for (row, column) in left_exits:
                if self.__board[row][column + 1] != 2:
                    valid = False
                    break
            if valid:
                moves.add((2, "left"))

        # If the cell on left is 2 for each exit position, then the move (2, right) is valid.
        elif right_exits:
            valid = True
            for (row, column) in right_exits:
                if self.__board[row][column - 1] != 2:
                    valid = False
                    break
            if valid:
                moves.add((2, "right"))

        return moves

    # Function to get the available moves based on the empty cells position.
    def getMoves(self) -> set:
        # We will store the moves of masterbrick towards the exit (-1) if there is any.
        moves: set = self.masterBrickMovesToExit()

        # Directions (up, down, left, right)
        directions: dict = {
            "up" : (-1, 0),
            "down" : (1, 0),
            "left" : (0, -1),
            "right" : (0, 1)
        }

        opposite_directions: dict = {
            "up" : "down",
            "left" : "right",
            "right" : "left",
            "down" : "up"
        }

        # Get the empty cells location.
        emptyCells: list = self.getEmptyCells()

        # We will check each direction and add whatever is valid to the moves list. Implement the check for masterbrick.
        for h, w in emptyCells:
            for direction, (row_offset, column_offset) in directions.items():
                new_row, new_column = (h + row_offset), (w + column_offset)

                # Check if new row and column are within bounds.
                if (0 <= new_row < self.__height) and (0 <= new_column < self.__width):
                    # Check if the location is wall or not (1).
                    if (self.__board[new_row][new_column] > 0) and (self.__board[new_row][new_column] != 1):
                        # Check the adjacents.
                        adjacents: set = self.checkAdjacent(new_row, new_column, self.__board[new_row][new_column])

                        # If no adjacents, it means the brick only takes one space and can be moved to any emty space.
                        if (len(adjacents) == 0):
                            moves.add((self.__board[new_row][new_column], opposite_directions[direction]))

                        else:
                            # We will now store unique rows and columns. This will help us figure out it the brick is horizontal or vertical.
                            rows: set = {location[0] for location in adjacents}
                            columns: set = {location[1] for location in adjacents}

                            # If there is one adjacent, we need to check if it's vertical or horizontal.
                            if (len(adjacents) == 1):
                                # If row is same, then horizonatal. If column is same then vertical.
                                # If horizontal, the brick can move freely to left/right empty spot.
                                # To move up or down, the brick needs two empty cells on its up/down.

                                # If vertical, the brick can move freely up/down on the empty spot.
                                # To move left/right, the brick needs two empty cells on its left/right.
                                
                                adjacent_row, adjacent_column = list(adjacents)[0]

                                # Check if the rows are same (means brick is horizontal).
                                if adjacent_row == new_row and adjacent_column != new_column:

                                    # Brick can freely move to left or right.
                                    if direction in ["left", "right"]:
                                        moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                    
                                    # Brick can only move up or down if two empty spaces.
                                    elif direction in ["up", "down"]:
                                        if (adjacent_row + directions[opposite_directions[direction]][0], adjacent_column) in emptyCells:
                                            moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                
                                # Else, check if columns are same (means brick is vertical).
                                elif (adjacent_column == new_column) and (adjacent_row != new_row):

                                    # Brick can freely move up and down.
                                    if direction in ["up", "down"]:
                                        moves.add((self.__board[new_row][new_column], opposite_directions[direction]))

                                    # Brick can only move left or right if two empty spaces.
                                    elif direction in ["left", "right"]:
                                        if (adjacent_row, adjacent_column + directions[opposite_directions[direction]][1]) in emptyCells:
                                            moves.add((self.__board[new_row][new_column], opposite_directions[direction]))


                            elif len(adjacents) >= 2:
                                # Still the brick could be either horizontal or vertical.
                                # Same logic as before, but: if horizontal, needs three empty spaces to move up/down. If vertical, needs three empty spaces to move left/right.
                                
                                # If rows set has only one item, then the brick is horizontal.
                                if len(rows) == 1:
                                    if direction in ["left", "right"]:
                                        moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                    
                                    elif direction in ["up", "down"]:
                                        for adjacent_column in columns:
                                            if (list(rows)[0] + directions[opposite_directions[direction]][0], adjacent_column) in emptyCells:
                                                moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                
                                # If only one item in columns set, then the brick is vertical.
                                elif len(columns) == 1:
                                    if direction in ["up", "down"]:
                                        moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                    
                                    elif direction in ["left", "right"]:
                                        for adjacent_row in rows:
                                            if (adjacent_row, list(columns)[0] + directions[opposite_directions[direction]][1]) in emptyCells:
                                                directions[opposite_directions[direction]][1]
                                
                                else:
                                    for adjacent_row, adjacent_column in adjacents:
                                        if (adjacent_row + directions[opposite_directions[direction]][0], adjacent_column + directions[opposite_directions[direction]][1]) in emptyCells:
                                            moves.add((self.__board[new_row][new_column], opposite_directions[direction]))

        return moves

    # Function to apply the moves.
    def applyMove(self, move: tuple) -> None:

        # Directions (up, down, left, right)
        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        # We will clone the board.
        new_board: list = self.cloneBoard()

        # Get the row and column offset and brick.
        row_offset, column_offset = directions[move[1]]
        direction: str = move[1]
        brick: int = move[0]

        found: bool = False

        # Find the location of the brick
        for h in range(self.__height):
            for w in range(self.__width):
                if new_board[h][w] == brick:
                    row_start, column_start = h, w
                    found = True
                    break
            
            if found:
                break
        
        # Also, if master brick is moved to exit (-1), swap -1 and 2 and fill the old place of 2 with 0.
        adjacents: set = self.checkAdjacent(row_start, column_start, move[0])
        new_row, new_column = (row_start + row_offset, column_start + column_offset)

        # List to store the location of empty cells before swapping.
        prev_empty_cells: list = []

        # List to store the location of empty cells after swapping.
        new_empty_cells: list = []

        if (0 <= new_row < self.__height) and (0 <= new_column < self.__width):

            # If no adjacents, it's a single cell brick and can be swapped without worrying about adjacent empty cells.
            if(len(adjacents) == 0):
                new_board[row_start][column_start], new_board[new_row][new_column] = new_board[new_row][new_column], new_board[row_start][column_start]
                prev_empty_cells.append((new_row, new_column))
                new_empty_cells.append((row_start, column_start))
            
            else:
                rows: set = {location[0] for location in adjacents}
                columns: set = {location[1] for location in adjacents}

                # Brick could be vertical or horizontal.
                if len(adjacents) == 1:
                    adjacent_row, adjacent_column = list(adjacents)[0]

                    # If the rows are same (means brick is horizontal).
                    if row_start == adjacent_row and column_start != adjacent_column:
                        # If going right, swap with min column. If going left, swap with max column.
                        if direction == "left":
                            new_board[row_start][adjacent_column], new_board[new_row][new_column] = new_board[new_row][new_column], new_board[row_start][adjacent_column]
                            prev_empty_cells.append((new_row, new_column))
                            new_empty_cells.append((row_start, adjacent_column))
                        
                        elif direction == "right":
                            new_board[row_start][column_start], new_board[row_start][adjacent_column + column_offset] = new_board[row_start][adjacent_column + column_offset], new_board[row_start][column_start]
                            prev_empty_cells.append((row_start, adjacent_column + column_offset))
                            new_empty_cells.append((row_start, column_start))
                        
                        # Swap each location.
                        elif direction in ["up", "down"]:
                            # Swap the initial tile.
                            new_board[row_start][column_start], new_board[new_row][new_column] = new_board[new_row][new_column], new_board[row_start][column_start]
                            prev_empty_cells.append((new_row, new_column))
                            new_empty_cells.append((row_start, column_start))

                            # Swap the adjacent brick with its corresponding empty cell.
                            new_board[adjacent_row][adjacent_column], new_board[adjacent_row + row_offset][adjacent_column + column_offset] = new_board[adjacent_row + row_offset][adjacent_column + column_offset], new_board[adjacent_row][adjacent_column]
                            prev_empty_cells.append((adjacent_row + row_offset, adjacent_column + column_offset))
                            new_empty_cells.append((adjacent_row, adjacent_column))
                    
                    # If the columns are same (means brick is vertical).
                    elif row_start != adjacent_row and column_start == adjacent_column:
                        # If going up, swap with max row. If going down, swap with min row.
                        if direction == "up":
                            new_board[max(row_start, adjacent_row)][column_start], new_board[new_row][new_column] = new_board[new_row][new_column], new_board[max(row_start, adjacent_row)][column_start]
                            prev_empty_cells.append((new_row, new_column))
                            new_empty_cells.append((max(row_start, adjacent_row), column_start))

                        elif direction == "down":
                            new_board[min(row_start, adjacent_row)][column_start], new_board[adjacent_row + row_offset][adjacent_column + column_offset] = new_board[adjacent_row + row_offset][adjacent_column + column_offset], new_board[min(row_start, adjacent_row)][column_start]
                            prev_empty_cells.append((adjacent_row + row_offset, adjacent_column + column_offset))
                            new_empty_cells.append((min(row_start, adjacent_row), column_start))

                        elif direction in ["left", "right"]:
                            # Swap the initial tile.
                            new_board[row_start][column_start], new_board[new_row][new_column] = new_board[new_row][new_column], new_board[row_start][column_start]
                            prev_empty_cells.append((new_row, new_column))
                            new_empty_cells.append((row_start, column_start))

                            # Swap the adjacent brick with its corresponding offset tile.
                            new_board[adjacent_row][adjacent_column], new_board[adjacent_row + row_offset][adjacent_column + column_offset] = new_board[adjacent_row + row_offset][adjacent_column + column_offset], new_board[adjacent_row][adjacent_column]
                            prev_empty_cells.append((adjacent_row + row_offset, adjacent_column + column_offset))
                            new_empty_cells.append((adjacent_row, adjacent_column))
                
                elif len(adjacents) >= 2:
                    #print(f"Adjacents = {len(adjacents)} and length of row is {len(rows)} and column is {len(columns)}.\n")
                    # If rows set has only one item, then the brick is horizontal.
                    if len(rows) == 1:
                        # If going right, swap with min column. If going left, swap with max column.
                        if direction == "left":
                            new_board[row_start][max(column_start, max(columns))], new_board[new_row][new_column] = new_board[new_row][new_column], new_board[row_start][max(column_start, max(columns))]
                            prev_empty_cells.append((new_row, new_column))
                            new_empty_cells.append((row_start, max(column_start, max(columns))))
                        
                        elif direction == "right":
                            new_board[row_start][min(column_start, min(columns))], new_board[row_start + row_offset][max(columns) + column_offset] = new_board[row_start + row_offset][max(columns) + column_offset], new_board[row_start][min(column_start, min(columns))]
                            prev_empty_cells.append((row_start + row_offset, max(columns) + column_offset))
                            new_empty_cells.append((row_start, min(column_start, min(columns))))
                        
                        elif direction in ["up", "down"]:
                            # Swap the initial tile.
                            new_board[row_start][column_start], new_board[new_row][new_column] = new_board[new_row][new_column], new_board[row_start][column_start]
                            prev_empty_cells.append((new_row, new_column))
                            new_empty_cells.append((row_start, column_start))

                            # Swap the rest of the adjacent bricks with its corresponding offset tile.
                            for col in columns:
                                new_board[row_start][col], new_board[row_start + row_offset][col + column_offset] = new_board[row_start + row_offset][col + column_offset], new_board[row_start][col]
                                prev_empty_cells.append((row_start + row_offset, col + column_offset))
                                new_empty_cells.append((row_start, col))
                    
                    # If columns set has only one item, then the brick is vertical.
                    elif len(columns) == 1:
                        # If going up, swap with max row. If going down, swap with min row.
                        if direction == "up":
                            new_board[max(rows)][column_start], new_board[new_row][new_column] = new_board[new_row][new_column], new_board[max(rows)][column_start]
                            prev_empty_cells.append((new_row, new_column))
                            new_empty_cells.append((max(rows), column_start))
                        
                        elif direction == "down":
                            new_board[min(row_start, min(rows))][column_start], new_board[max(rows) + row_offset][column_start] = new_board[max(rows) + row_offset][column_start], new_board[min(row_start, min(rows))][column_start]
                            prev_empty_cells.append((max(rows) + row_offset, column_start))
                            new_empty_cells.append((min(row_start, min(rows)), column_start))
                        
                        elif direction in ["left", "right"]:
                            # Swap the initial tile.
                            new_board[row_start][column_start], new_board[new_row][new_column] = new_board[new_row][new_column], new_board[row_start][column_start]
                            prev_empty_cells.append((new_row, new_column))
                            new_empty_cells.append((row_start, column_start))

                            # Swap the rest of the adjacent bricks with its corresponding offset tile.
                            for r in rows:
                                new_board[r][column_start], new_board[r + row_offset][column_start + column_offset] = new_board[r + row_offset][column_start + column_offset],  new_board[r][column_start]
                                prev_empty_cells.append((r + row_offset, column_start + column_offset))
                                new_empty_cells.append((r, column_start))

                    else:
                        # We will add the first position of the brick in adjacents set because we might need to swap it.
                        adjacents.add((row_start, column_start))

                        # Update the rows and columns set.
                        rows: set = {location[0] for location in adjacents}
                        columns: set = {location[1] for location in adjacents}

                        if direction == "left":
                            for r in rows:
                                new_board[r][max(columns)], new_board[r + row_offset][min(columns) + column_offset] = new_board[r + row_offset][min(columns) + column_offset], new_board[r][max(columns)]
                                prev_empty_cells.append((r + row_offset, min(columns) + column_offset))
                                new_empty_cells.append((r, max(columns)))
                        
                        elif direction == "right":
                            for r in rows:
                                new_board[r][min(columns)], new_board[r + row_offset][max(columns) + column_offset] = new_board[r + row_offset][max(columns) + column_offset], new_board[r][min(columns)]
                                prev_empty_cells.append((r + row_offset, max(columns) + column_offset))
                                new_empty_cells.append((r, min(columns)))
                        
                        elif direction == "up":
                            for col in columns:
                                new_board[max(rows)][col], new_board[min(rows) + row_offset][col + column_offset] = new_board[min(rows) + row_offset][col + column_offset], new_board[max(rows)][col]
                                prev_empty_cells.append((min(rows) + row_offset, col + column_offset))
                                new_empty_cells.append((max(rows), col))
                        
                        elif direction == "down":
                            for col in columns:
                                new_board[min(rows)][col], new_board[max(rows) + row_offset][col + column_offset] = new_board[max(rows) + row_offset][col + column_offset], new_board[min(rows)][col]
                                prev_empty_cells.append((max(rows) + row_offset, col + column_offset))
                                new_empty_cells.append((min(rows), col))

        self.__board = new_board
        self.updateEmptyCells(prev_empty_cells, new_empty_cells)

        # If brick that was moved was master brick, then we need to check if it reached the goal.
        # If -1 is not in the border and is inside somewhere because it got swapped, change -1 to 0. 
        # The board won't have -1 at all which indicates goal condition.
        if brick == 2:
            for h in range(self.__height):
                for w in range(self.__width):
                    if self.__board[h][w] == -1:
                        if not (h == 0 or h == self.__height - 1 or w == 0 or w == self.__width - 1):
                            self.__board[h][w] = 0

    # swapIdx function used by normalize().
    def swapIdx(self, index_1: int, index_2: int) -> None:
        for r in range(self.__height):
            for c in range(self.__width):
                if self.__board[r][c] == index_1:
                    self.__board[r][c] = index_2
                
                elif self.__board[r][c] == index_2:
                    self.__board[r][c] = index_1

    # Function to normalize the board.
    def normalize(self) -> None:
        next_index: int = 3

        for h in range(self.__height):
            for w in range(self.__width):
                if self.__board[h][w] == next_index:
                    next_index += 1
                
                elif self.__board[h][w] > next_index:
                    self.swapIdx(next_index, self.__board[h][w])
                    next_index += 1


# Function to compare the state of two boards.
def compareState(sliding_brick_1: SlidingBrick, sliding_brick_2: SlidingBrick) -> bool:
    if (sliding_brick_1.getHeight() != sliding_brick_2.getHeight()) or (sliding_brick_1.getWidth() != sliding_brick_2.getWidth()):
        print("Error: Cannot compare boards with different dimensions.")
        sys.exit(1)
    
    board_1: list = sliding_brick_1.getBoard()
    board_2: list = sliding_brick_2.getBoard()

    for h in range(sliding_brick_1.getHeight()):
        for w in range(sliding_brick_1.getWidth()):
            if board_1[h][w] != board_2[h][w]:
                return False
    
    return True

# Function that tests everything and reaches the goal state.
def randomWalk(sliding_brick: SlidingBrick, N: int):
    """
    1) generate all the moves that can be generated in the board,  
    2) select one at random,  
    3) execute it,  
    4) normalize the resulting game state, 
    5) if we have reached the goal, or if we have executed N moves, stop; otherwise, go back to 1. 
    """

    for i in range(N):
        # Generate all the moves available in the board.
        available_moves: set = sliding_brick.getMoves()

        # Select a random move.
        random_move: tuple = random.choice(list(available_moves))

        # Print the random move executed and the board state.
        print(f"\n({random_move[0]}, {random_move[1]})")

        # Execute the random move.
        sliding_brick.applyMove(random_move)

        # Normalize the resulting game state.
        sliding_brick.normalize()

        # Print the board.
        sliding_brick.printBoard()

        # Check if we are in goal state.
        if (sliding_brick.isGoalState()) or (i == N - 1):
            break

# Function to load the game from the file and create the Sliding Brick instance and then print the board.
def loadGame(filename) -> SlidingBrick:
    with open(filename, "r") as fp:
        # First line contains the width and height.
        parts = fp.readline().strip().split(",")
        width: int = int(parts[0])
        height: int = int(parts[1])

        # From second line is the board.
        board: list = []

        # Each line has the item of the board. We will add it to the board row by row.
        for line in fp:
            row: list = []
            board_items = line.strip().split(",")

            for item in board_items:
                if item.strip():
                    row.append(int(item))
            
            board.append(row)
    
    # Now that we have the board, we will create an instance of our class
    sliding_brick = SlidingBrick(width, height, board)
    return sliding_brick

# Function to convert the board state from list to tuple since sets don't store lists. Set needs non mutable object to hash it.
def tuple_board(board: list) -> tuple:
    return tuple(tuple(row) for row in board)

# Function that applies BFS.
def BFSTraversal(board_state: SlidingBrick):
    # Add the initial board state to queue and set.
    queue: list = [board_state]
    front_pointer: int = 0

    visited_states: set = set()
    visited_states.add(tuple_board(board_state.getBoard()))

    # Variable to keep track of total nodes visited.
    total_nodes: int = 0

    while front_pointer < len(queue):
        current_state: SlidingBrick = queue[front_pointer]
        front_pointer += 1
        total_nodes += 1

        # If current state is the goal state, then we will return the parent-child heirarchy to the goal state.
        if current_state.isGoalState():
            solution_path: list = []

            while current_state is not None:
                solution_path.append(current_state)
                current_state = current_state.getParent()

            # Since the heirarchy will be from goal to initial, we need to reverse to get from initial to goal.
            solution_path.reverse()

            # Return the solution path.
            return solution_path, total_nodes
        
        # Apply each available moves of the current state.
        for move in current_state.getMoves():
            # Create a new board state.
            new_state: SlidingBrick = SlidingBrick(current_state.getWidth(), current_state.getHeight(), current_state.cloneBoard())

            # Copy the empty cells location from current to the new_state.
            new_state.setEmptyCells(current_state.getEmptyCells())

            # Copy the exit positions from current to new_state.
            new_state.setExitPositions(current_state.getExitPositions())

            # Apply each available move.
            new_state.applyMove(move)

            # Normalize the new state.
            new_state.normalize()

            # Get the tuple board.
            new_state_tuple = tuple_board(new_state.getBoard())

            if new_state_tuple not in visited_states:
                # Set the current state as the new state's parent.
                new_state.setParent(current_state)

                # Set the move tha led current state to new state.
                new_state.setMove(move)

                # Add the new_state to visited_states set and queue.
                visited_states.add(new_state_tuple)
                queue.append(new_state)
    
    # At this point, there is no solution.
    return None, total_nodes

# Function that applies DFS. stack method.
def DFSTraversal(board_state: SlidingBrick):
    # Add the initial board to stack and set.
    stack: list = [board_state]

    visited_states: set = set()
    visited_states.add(tuple_board(board_state.getBoard()))

    # Variable to keep track of the total nodes explored.
    total_nodes: int = 0

    while stack:
        current_state: SlidingBrick = stack.pop()
        total_nodes += 1

        # If current state is the goal state, then we will return the parent-child heirarchy to the goal state.
        if current_state.isGoalState():
            solution_path: list = []

            while current_state is not None:
                solution_path.append(current_state)
                current_state = current_state.getParent()

            # Since the heirarchy will be from goal to initial, we need to reverse to get from initial to goal.
            solution_path.reverse()

            return solution_path, total_nodes
        
        # Apply each available moves of the current state.
        for move in current_state.getMoves():
            # Create a new_state.
            new_state: SlidingBrick = SlidingBrick(current_state.getWidth(), current_state.getHeight(), current_state.cloneBoard())

            # Copy the empty cells location from current to the new_state.
            new_state.setEmptyCells(current_state.getEmptyCells())

            # Copy the exit positions from current to new_state.
            new_state.setExitPositions(current_state.getExitPositions())            

            # Apply the move.
            new_state.applyMove(move)

            # Normalize the new state.
            new_state.normalize()

            # Get the tuple board since sets don't store lists.
            new_state_tuple: tuple = tuple_board(new_state.getBoard())

            # Add the new_state to set and stack if not visited.
            if new_state_tuple not in visited_states:
                new_state.setParent(current_state)      # Set the parent of this new_state to current_state.
                new_state.setMove(move)                 # Set the move of this new_state to the move which led to this new_state.
                visited_states.add(new_state_tuple)
                stack.append(new_state)
    
    return None, total_nodes

# Search function for IDS according to the depth. Recrusively search the board until depth times.
def DLS(current_state: SlidingBrick, visited_states: dict, depth: int, level: int):
    nodes_count = 1

    if current_state.isGoalState():
        return [current_state], nodes_count
    
    if depth == 0:
        return None, nodes_count

    for move in current_state.getMoves():
        # Create a new_state.
        new_state: SlidingBrick = SlidingBrick(current_state.getWidth(), current_state.getHeight(), current_state.cloneBoard())

        # Copy the empty cells location from current to the new_state.
        new_state.setEmptyCells(current_state.getEmptyCells())     

        # Copy the exit positions from current to new_state.
        new_state.setExitPositions(current_state.getExitPositions())       

        # Apply the move.
        new_state.applyMove(move)

        # Normalize the new state.
        new_state.normalize()

        # Get the tuple board since sets don't store lists.
        new_state_tuple: tuple = tuple_board(new_state.getBoard())
        new_level = level + 1

        if new_state_tuple not in visited_states or new_level < visited_states[new_state_tuple]:
            visited_states[new_state_tuple] = new_level     # Add to the set.
            new_state.setParent(current_state)              # Set the parent of this new_state to current_state.
            new_state.setMove(move)                         # Set the move of this new_state to the move which led to this new_state.

            # Recursively call DLS.
            solution_path, nodes = DLS(new_state, visited_states, depth - 1, new_level)

            # Increment the nodes_count from the return value of previous calls.
            nodes_count += nodes

            # Add the solution path from previous recursive call to current call.
            if solution_path is not None:
                return [current_state] + solution_path, nodes_count
            
            # Not sure if this line is needed. Code is really slow because of this.
            # else:
            #     del visited_states[new_state_tuple]
            
    return None, nodes_count

# Function that applies IDS. Recursive method.
def IDSTraversal(board_state: SlidingBrick):
    total_nodes: int = 0
    depth: int = 0

    solution_path: list = []

    # Keep increasing the depth until we find the goal. from depth = 0 to infinity
    while True:
        visited_states: dict = {}
        
        initial_board_tuple: tuple = tuple_board(board_state.getBoard())
        visited_states[initial_board_tuple] = 0

        solution_path, nodes_count = DLS(board_state, visited_states, depth, 0)

        total_nodes += nodes_count
    
        if solution_path is not None:
            return solution_path, total_nodes
        
        depth += 1

# Heuristic function. Manhattan distance.
def heuristic(board_state: SlidingBrick) -> int:
    master_brick_positions: list = board_state.getMasterBrickPositions()
    exit_positions: list = board_state.getExitPositions()

    # Calculate the manhattan distance.
    manhattan_dist = float('inf')
    for (master_row, master_column) in master_brick_positions:
        for (exit_row, exit_column) in exit_positions:
            distance: int = abs(master_row - exit_row) + abs(master_column - exit_column)
            if distance < manhattan_dist:
                manhattan_dist = distance
    
    return manhattan_dist

# Function that applies A*.
def AStarTraversal(board_state: SlidingBrick):
    total_nodes: int = 0
    
    # Using a counter in case the f(n) for previous state and new_state equals.
    counter: int = 0

    # Min heap/priority queue.
    min_heap = PriorityQueue()

    # Add initial board's path cost, that is 0.
    path_and_cost: dict = {tuple_board(board_state.getBoard()) : 0}

    # f(n) = path_cost + heuristic
    initial_f: int = heuristic(board_state)

    # Add the initial board to the heap and set.
    min_heap.put((initial_f, 0, counter, board_state))
    counter += 1

    visited_states: set = set()

    while min_heap:
        current_state: SlidingBrick = None      # Placeholder for the board_states that will be popped from the heap.

        current_f, current_path_cost, count, current_state = min_heap.get()
        total_nodes += 1
        current_tuple = tuple_board(current_state.getBoard())

        if current_tuple in visited_states:
            continue

        visited_states.add(current_tuple)

        # If current state is the goal state, then we will return the parent-child heirarchy to the goal state.
        if current_state.isGoalState():
            solution_path: list = []

            while current_state is not None:
                solution_path.append(current_state)
                current_state = current_state.getParent()

            # Since the heirarchy will be from goal to initial, we need to reverse to get from initial to goal.
            solution_path.reverse()

            return solution_path, total_nodes
        
        for move in current_state.getMoves():
            # Create a new_state.
            new_state: SlidingBrick = SlidingBrick(current_state.getWidth(), current_state.getHeight(), current_state.cloneBoard())

            # Copy the empty cells location from current to the new_state.
            new_state.setEmptyCells(current_state.getEmptyCells())    

            # Copy the exit positions from current to new_state.
            new_state.setExitPositions(current_state.getExitPositions())    

            # Apply the move.
            new_state.applyMove(move)

            # Normalize the new state.
            new_state.normalize()

            # Get the tuple board since sets don't store lists.
            new_state_tuple: tuple = tuple_board(new_state.getBoard())

            # Add the new_state to set and stack if not visited.
            new_path_cost: int = current_path_cost + 1

            if new_state_tuple not in path_and_cost or new_path_cost < path_and_cost[new_state_tuple]:
                new_state.setParent(current_state)      # Set the parent of this new_state to current_state.
                new_state.setMove(move)                 # Set the move of this new_state to the move which led to this new_state.
                path_and_cost[new_state_tuple] = new_path_cost
                new_f: int = new_path_cost + heuristic(new_state)
                min_heap.put((new_f, new_path_cost, counter, new_state))
                counter += 1
    
    # At this point, there is no solution.
    return None, total_nodes


# Main function.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sh run.sh <command> [<optional-argument>]")
        sys.exit(1)

    command: str = sys.argv[1]

    if command == "print":
        if len(sys.argv) < 3:
            print(f"Usage: sh run.sh print <file.txt>")
            sys.exit(1)

        filename: str = sys.argv[2]

        # Load the game.
        sliding_brick: SlidingBrick = loadGame(filename)

        # Print the board.
        sliding_brick.printBoard()

    elif command == "done":
        if len(sys.argv) < 3:
            print(f"Usage: sh run.sh done <file.txt>")
            sys.exit(1)

        filename: str = sys.argv[2]

        # Load the game.
        sliding_brick: SlidingBrick = loadGame(filename)

        # Check if we are in goal state.
        print(sliding_brick.isGoalState())

    elif command == "availableMoves":
        if len(sys.argv) < 3:
            print(f"Usage: sh run.sh availableMoves <file.txt>")
            sys.exit(1)

        filename: str = sys.argv[2]

        # Load the game and find the empty cells (0) and where exits (-1) are.
        sliding_brick: SlidingBrick = loadGame(filename)
        sliding_brick.findEmptyCells()
        sliding_brick.findExitPositions()

        # Get the valid moves.
        moves: list = sliding_brick.getMoves()

        if not moves:
            print("No moves")
        
        else:
            for move in moves:
                print(f"({move[0]}, {move[1]})")
    
    elif command == "applyMove":
        if len(sys.argv) < 4:
            print(f"Usage: sh run.sh applyMove <file.txt> <(brick, direction)>")
            sys.exit(1)

        filename: str = sys.argv[2]

        move_str: str = sys.argv[3][1 : -1]

        parts = move_str.split(", ")

        if len(parts) == 2:
            try:
                brick = int(parts[0])
                direction = str(parts[1])
                move: tuple = (brick, direction)
            except ValueError:
                print("Error: The brick number should be an integer.")
                sys.exit(1)
        else:
            print("Error: Invalid format. Expected (brick_number, direction).")
            sys.exit(1)
        
        # Load the game and find the empty cells (0) and where exits (-1) are.
        sliding_brick: SlidingBrick = loadGame(filename)
        sliding_brick.findEmptyCells()
        sliding_brick.findExitPositions()

        # Apply the move.
        sliding_brick.applyMove(move)

        # Print the board.
        sliding_brick.printBoard()

    elif command == "compare":
        if len(sys.argv) < 4:
            print(f"Usage: sh run.sh compare <file_1.txt> <file_2.txt>")
            sys.exit(1)
        
        file_1: str = sys.argv[2]

        file_2: str = sys.argv[3]

        try:
            sliding_brick_1: SlidingBrick = loadGame(file_1)
            sliding_brick_2: SlidingBrick = loadGame(file_2)
        except FileNotFoundError:
            print("Error: One of the files doesn't exist.")
            sys.exit(1)
        
        print(compareState(sliding_brick_1, sliding_brick_2))
    
    elif command == "norm":
        if len(sys.argv) < 3:
            print(f"Usage: sh run.sh norm <file.txt>")
            sys.exit(1)
        
        filename: str = sys.argv[2]

        sliding_brick: SlidingBrick = loadGame(filename)

        # Normalize the board.
        sliding_brick.normalize()

        # Print the board.
        sliding_brick.printBoard()

    elif command == "random":
        if len(sys.argv) < 4:
            print(f"Usage: sh run.sh random <file.txt> <N>")
            sys.exit(1)
        
        filename: str = sys.argv[2]
        iterations: int = int(sys.argv[3])

        # Load the game and find the empty cells (0) and where exits (-1) are.
        sliding_brick: SlidingBrick = loadGame(filename)
        sliding_brick.findEmptyCells()
        sliding_brick.findExitPositions()

        sliding_brick.printBoard()

        # Call the randomWalk function.
        randomWalk(sliding_brick, iterations)
    
    elif command == "bfs":
        if len(sys.argv) < 3:
            print(f"Usage: sh run.sh bfs <file.txt>")
            sys.exit(1)
        
        filename: str = sys.argv[2]

        # Load the game and find the empty cells (0) and where exits (-1) are.
        board_state: SlidingBrick = loadGame(filename)
        board_state.findEmptyCells()
        board_state.findExitPositions()

        start = time.time()
        solution_path, total_nodes = BFSTraversal(board_state)
        end = time.time()

        if solution_path is None:
            print("This board has no solutions!")
        
        else:
            state: SlidingBrick = None
            for state in solution_path:
                move = state.getStateMove()

                if move is not None:
                    print(f"({move[0]},{move[1]})")
            
            print()
            state.printBoard()

            print()
            print(total_nodes)
            print(f"{end - start:.2f}")
            print(len(solution_path) - 1)   # Solution path has initial board, which should not be counted in length of solution.

    elif command == "dfs":
        if len(sys.argv) < 3:
            print(f"Usage: sh run.sh dfs <file.txt>")
            sys.exit(1)
        
        filename: str = sys.argv[2]

        # Load the game and find the empty cells (0) and where exits (-1) are.
        board_state: SlidingBrick = loadGame(filename)
        board_state.findEmptyCells()
        board_state.findExitPositions()

        start = time.time()
        solution_path, total_nodes = DFSTraversal(board_state)
        end = time.time()

        if solution_path is None:
            print("This board has no solutions!")
        
        else:
            state: SlidingBrick = None
            for state in solution_path:
                move = state.getStateMove()

                if move is not None:
                    print(f"({move[0]},{move[1]})")
            
            print()
            state.printBoard()

            print()
            print(total_nodes)
            print(f"{end - start:.2f}")
            print(len(solution_path) - 1)   # Solution path has initial board, which should not be counted in length of solution.

    elif command == "ids":
        if len(sys.argv) < 3:
            print(f"Usage: sh run.sh ids <file.txt>")
            sys.exit(1)
        
        filename: str = sys.argv[2]

        # Load the game and find the empty cells (0) and where exits (-1) are.
        board_state: SlidingBrick = loadGame(filename)
        board_state.findEmptyCells()
        board_state.findExitPositions()

        start = time.time()
        solution_path, total_nodes = IDSTraversal(board_state)
        end = time.time()

        if solution_path is None:
            print("This board has no solutions!")
        
        else:
            state: SlidingBrick = None
            for state in solution_path:
                move = state.getStateMove()

                if move is not None:
                    print(f"({move[0]},{move[1]})")
            
            print()
            state.printBoard()

            print()
            print(total_nodes)
            print(f"{end - start:.2f}")
            print(len(solution_path) - 1)   # Solution path has initial board, which should not be counted in length of solution.
    
    elif command == "astar":
        if len(sys.argv) < 3:
            print(f"Usage: sh run.sh astar <file.txt>")
            sys.exit(1)
        
        filename: str = sys.argv[2]

        # Load the game and find the empty cells (0) and where exits (-1) are.
        board_state: SlidingBrick = loadGame(filename)
        board_state.findEmptyCells()
        board_state.findExitPositions()

        start = time.time()
        solution_path, total_nodes = AStarTraversal(board_state)
        end = time.time()

        if solution_path is None:
            print("This board has no solutions!")
        
        else:
            state: SlidingBrick = None
            for state in solution_path:
                move = state.getStateMove()

                if move is not None:
                    print(f"({move[0]},{move[1]})")
            
            print()
            state.printBoard()

            print()
            print(total_nodes)
            print(f"{end - start:.2f}")
            print(len(solution_path) - 1)   # Solution path has initial board, which should not be counted in length of solution.

    else:
        print(f"Error: Unknown command '{command}'.")
        sys.exit(1)
