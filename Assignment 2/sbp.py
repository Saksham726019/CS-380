import sys

class SlidingBrick:
    def __init__(self, w, h, board):
        self.__width:int = w
        self.__height:int = h
        self.__board:list = board
        self.__masterPosition:int = 0
    
    def printBoard(self):
        print(f"{self.__width}, {self.__height},")

        # Add each item of the board to the items:str.
        items:str = ""
        for item in self.__board:
            items += f"{item},"
        
        print(items)


# Function to load the game from the file and create the Sliding Brick instance and then print the board.
def loadGame(filename) -> SlidingBrick:
    with open(filename, "r") as fp:
        # First line contains the width and height.
        parts = fp.readline().strip().split(",")
        width:int = int(parts[0])
        height:int = int(parts[1])

        # From second line is the board.
        board:list = []

        # Each line has the item of the board. We will add it to the board row by row.
        for line in fp:
            row:list = []
            board_items = line.strip().split(",")

            for item in board_items:
                row.append(int(item))
            
            board.append(row)
    
    # Now that we have the board, we will create an instance of our class
    sliding_brick_puzzle = SlidingBrick(width, height, board)
    return sliding_brick_puzzle


# Main function.
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sbp.py <command> [<filename>]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "print":
        if len(sys.argv) < 3:
            print("Error: Missing filename for 'print' command.")
            sys.exit(1)
        filename = sys.argv[2]

        # Let's load the game.
        sliding_brick_puzzle:SlidingBrick = loadGame(filename)

        # Print the board.
        sliding_brick_puzzle.printBoard()
    else:
        print(f"Error: Unknown command '{command}'.")
        sys.exit(1)
