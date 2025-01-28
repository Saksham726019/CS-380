import sys

class SlidingBrick:
    def __init__(self, w, h, board):
        self.__width: int = w
        self.__height: int = h
        self.__board: list = board
        self.__masterBrickPosition: int = 0
    
    def getBoard(self) -> list:
        return self.__board
    
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
            print("Error: Missing filename for 'print' command.")
            sys.exit(1)

        filename: str = sys.argv[2]

        # Load the game.
        sliding_brick: SlidingBrick = loadGame(filename)

        # Print the board.
        sliding_brick.printBoard()

    elif command == "done":
        if len(sys.argv) < 3:
            print("Error: Missing filename for 'done' command.")
            sys.exit(1)

        filename: str = sys.argv[2]

        # Load the game.
        sliding_brick: SlidingBrick = loadGame(filename)

        # Check if we are in goal state.
        print(sliding_brick.isGoalState())

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

