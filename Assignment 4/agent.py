import math
import random

import game
import othello

class HumanPlayer(game.Player):
    def __init__(self):
        super().__init__()

    def choose_move(self, state: othello.State) -> othello.State:
        # generate the list of moves:
        moves: list = state.generateMoves()

        for i, action in enumerate(moves):
            print('{}: {}'.format(i, action))
        response = input('Please choose a move: ')
        return moves[int(response)]


class RandomAgent(game.Player):
    def __init__(self):
        super().__init__()

    # Function that gets the Othello state, generates the available move and returns a randomly choosen move.
    def choose_move(self, state: othello.State) -> othello.OthelloMove:
        moves: list = state.generateMoves()

        if not moves:
            return None
        
        return random.choice(moves)



class MinimaxAgent(game.Player):
    pass


class AlphaBeta(game.Player):
    pass