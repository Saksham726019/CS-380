import sys

class SlidingBrick:
    def __init__(self, w, h, board):
        self.__width: int = w
        self.__height: int = h
        self.__board: list = board
        self.__emptyCells: list = []  # Store (row/height, column/width) tuple in this list.
        self.__masterBrickPosition: int = 0
    
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
    
    # Function to get the available moves based on the empty cells position.
    def getMoves(self) -> list:
        moves: list = []    # We'll store valid moves in this list.

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
            for direction, (row, column) in directions.items():
                new_row, new_column = (h + row), (w + column)

                # Check if new row and column are within bounds.
                if (0 <= new_row < self.__height) and (0 <= new_column < self.__width):
                    # Check if the location is wall or not (1).
                    if (self.__board[new_row][new_column] > 0) and (self.__board[new_row][new_column] != 1):
                        # Check if the location is not a master brick.
                        if (self.__board[new_row][new_column] != 2):
                            moves.append((self.__board[new_row][new_column], opposite_directions[direction]))

                            # If the location is master brick, we can only move certain direction based on how master brick is on the board.
                        elif (self.__board[new_row][new_column] == 2):
                            pass

        
        return moves


# Function to copy and return the initial (original) board.
def cloneOriginalBoard(sliding_brick: SlidingBrick) -> list:
    original_board: list = []

    for row in sliding_brick.getBoard():
        original_board.append(row[:])

    return original_board

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
            print(f"Error: Missing filename for {command} command.")
            sys.exit(1)

        filename: str = sys.argv[2]

        # Load the game.
        sliding_brick: SlidingBrick = loadGame(filename)

        # Print the board.
        sliding_brick.printBoard()

    elif command == "done":
        if len(sys.argv) < 3:
            print(f"Error: Missing filename for {command} command.")
            sys.exit(1)

        filename: str = sys.argv[2]

        # Load the game.
        sliding_brick: SlidingBrick = loadGame(filename)

        # Check if we are in goal state.
        print(sliding_brick.isGoalState())

    elif command == "availableMoves":
        if len(sys.argv) < 3:
            print(f"Error: Missing filename for {command} command.")
            sys.exit(1)

        filename: str = sys.argv[2]

        # Load the game.
        sliding_brick: SlidingBrick = loadGame(filename)

        # Get the valid moves.
        moves: list = sliding_brick.getMoves()

        # Print the moves.
        for move in moves:
            print(f"({move[0]}, {move[1]})")

    else:
        print(f"Error: Unknown command '{command}'.")
        sys.exit(1)

    original_board: list = cloneOriginalBoard(sliding_brick)

    # # Test. Remove later
    # print("\nCloned Original board")
    # for row in original_board:
    #     items: str = ""
    #     for item in row:
    #         items += str(item) + ", "
    #     print(items)

    # Test. Remove later
    # print(f"\nEmpty cells: {sliding_brick.getEmptyCells()}")
