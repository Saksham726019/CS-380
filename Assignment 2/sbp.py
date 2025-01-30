import sys

class SlidingBrick:
    def __init__(self, w: int, h: int, board: list):
        self.__width: int = w
        self.__height: int = h
        self.__board: list = board
        self.__emptyCells: list = []  # Store (row/height, column/width) tuple in this list.
        self.__masterBrickPositions: list = []
    
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
            
            print(items)
    
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
    
    # Function to find empty cells (0) in the board.
    def findEmptyCells(self) -> None:
        for h in range(self.__height):
            for w in range(self.__width):
                if self.__board[h][w] == 0:
                    self.__emptyCells.append((h, w))
    
    # Function to return the empty cells location.
    def getEmptyCells(self) -> list:
        self.__emptyCells.clear()
        self.findEmptyCells()
        return self.__emptyCells
    
    # Function to find the master brick (2) in the board.
    def findMasterBrick(self) -> None:
        for h in range(self.__height):
            for w in range(self.__width):
                if self.__board[h][w] == 2:
                    self.__masterBrickPositions.append((h, w))
    
    # Functon to return master brick locations in the board.
    def getMasterBrickPositions(self) -> list:
        self.__masterBrickPositions.clear()
        self.findMasterBrick()
        return self.__masterBrickPositions

    # Function to check if adjacent cells are the same valued bricks.
    def checkAdjacent(self, h: int, w: int, brick: int) -> set:
        # Directions (up, down, left, right)
        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        adjacent = set()        # Use a set to store unique positions.
        queue: list = [(h, w)]  # Store the locations as we traverse using bfs.

        for direction, (row_offset, col_offset) in directions.items():
            front_pointer: int = 0

            while front_pointer < len(queue):
                row, col = queue[front_pointer]

                new_row = row + row_offset
                new_col = col + col_offset

                # Check if the new location is within boundaries.
                if 0 <= new_row < self.__height and 0 <= new_col < self.__width:
                    # If it's the same brick, then add the location to set and continue in the same direction.
                    if self.__board[new_row][new_col] == brick:
                        adjacent.add((new_row, new_col))
                        queue.append((new_row, new_col))
                        front_pointer += 1
                    else:
                        break  # We no longer need to go in that direction if different brick is found.

        return adjacent

    # Function to get the moves of masterbrick towards the exit (-1) if there is any.
    def masterBrickMovesToExit(self) -> set:
        # Get the master brick locations.
        master_brick_locations: list = self.getMasterBrickPositions()

        # Directions (up, down, left, right)
        directions: dict = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        moves = set()

        # Check all positions of the master brick.
        for h, w in master_brick_locations:
            for direction, (row_offset, col_offset) in directions.items():
                new_row, new_col = h + row_offset, w + col_offset

                # Check if the new position is within bounds and is an exit.
                if 0 <= new_row < self.__height and 0 <= new_col < self.__width:
                    if self.__board[new_row][new_col] == -1:
                        moves.add((2, direction))

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


                            elif (len(adjacents) == 2):
                                # Still the brick could be either horizontal or vertical.
                                # Same logic as before, but: if horizontal, needs three empty spaces to move up/down. If vertical, needs three empty spaces to move left/right.
                                
                                # If rows set has only one item, then the brick is horizontal.
                                if len(rows) == 1:
                                    if direction in ["left", "right"]:
                                        moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                    
                                    elif direction in ["up", "down"]:
                                        for adjacent_column in columns:
                                            if (rows.pop()[0] + directions[opposite_directions[direction]][0], adjacent_column) in emptyCells:
                                                moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                
                                # If only one item in columns set, then the brick is vertical.
                                elif len(columns) == 1:
                                    if direction in ["up", "down"]:
                                        moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                    
                                    elif direction in ["left", "right"]:
                                        for adjacent_row in rows:
                                            if (adjacent_row, columns.pop()[0] + directions[opposite_directions[direction]][1]) in emptyCells:
                                                directions[opposite_directions[direction]][1]

                            elif (len(adjacents) >= 3):
                                # The board can only be rectangle or squared, could only be horizontal or vertical.
                                # The logic is same. But, might need different number of spaces on either way, depending on how much space it takes horizontally and vertically.
                                
                                if len(rows) == 1:
                                    if direction in ["left", "right"]:
                                        moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                    
                                    elif direction in ["up", "down"]:
                                        for adjacent_column in columns:
                                            if (rows.pop()[0] + directions[opposite_directions[direction]][0], adjacent_column) in emptyCells:
                                                moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                
                                elif len(columns) == 1:
                                    if direction in ["up", "down"]:
                                        moves.add((self.__board[new_row][new_column], opposite_directions[direction]))
                                    
                                    elif direction in ["left", "right"]:
                                        for adjacent_row in rows:
                                            if (adjacent_row, columns.pop()[0] + directions[opposite_directions[direction]][1]) in emptyCells:
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

        # Get the row and column offset.
        row_offset, column_offset = directions[move[1]]
        found: bool = False

        # Find the location of the brick
        for h in range(self.__height):
            for w in range(self.__width):
                if new_board[h][w] == move[0]:
                    new_row, new_column = (h + row_offset), (w + column_offset)
                    found = True
                    break
            
            if found:
                break
        
        if (0 <= new_row < self.__height) and (0 <= new_column < self.__width):
            print(f"Swapping ({h}, {w}) with ({new_row}, {new_column})")
            new_board[h][w], new_board[new_row][new_column] = new_board[new_row][new_column], new_board[h][w]
        
        self.__board = new_board
        self.printBoard()


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

        # Load the game.
        sliding_brick: SlidingBrick = loadGame(filename)

        # Get the valid moves.
        moves: list = sliding_brick.getMoves()

        # Print the moves.
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
        
        # Load the game.
        sliding_brick: SlidingBrick = loadGame(filename)

        # Apply the move.
        sliding_brick.applyMove(move)

    else:
        print(f"Error: Unknown command '{command}'.")
        sys.exit(1)

    # # Test. Remove later
    # original_board: list = cloneOriginalBoard(sliding_brick)
    # print("\nCloned Original board")
    # for row in original_board:
    #     items: str = ""
    #     for item in row:
    #         items += str(item) + ", "
    #     print(items)

    # Test. Remove later
    # print(f"\nEmpty cells: {sliding_brick.getEmptyCells()}")

    # Test. Remove later
    # board: list = sliding_brick.getBoard()
    # print(f"Finding adjacents for {board[4][2]}")
    # print(f"Adjacent set:\n{sliding_brick.checkAdjacent(4, 2, 8)}")
    
    # Test. Remove later
    # moves: set = sliding_brick.getMoves()
    # # Print the moves.
    # for move in moves:
    #     print(f"({move[0]}, {move[1]})")

    # Test. Remove later
    # moves: set = sliding_brick.masterBrickMovesToExit()
    # for move in moves:
    #     print(f"({move[0]}, {move[1]})")
