import math
import random

import game
import othello

class HumanPlayer(game.Player):
    def __init__(self):
        super().__init__()

    def choose_move(self, state: othello.State) -> othello.OthelloMove:
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
    def __init__(self, depth: int):
        super().__init__()
        self.__depth: int = depth

    # Function that uses standard minimax algorithm to help choose our AI the best move. Evaluation function is the score.
    # We will use the tree with max as root as we want the move that gives the agent the max score.
    def minimax(self, current_state: othello.State, depth: int, max_turn: bool) -> int:
        # Base case: if we looked over all the depth or figured out a game over move.
        if depth == 0 or current_state.game_over():
            return current_state.score()
        
        moves: list = current_state.generateMoves()

        if max_turn:
            max_score: int = -math.inf

            for move in moves:
                # Apply each move, get its score and update the max score recursively.
                new_state: othello.State = current_state.applyMoveCloning(move)
                score: int = self.minimax(new_state, depth - 1, False)
                max_score = max(max_score, score)
            
            return max_score
        
        else:
            min_score: int = math.inf

            for move in moves:
                # Apply each move, get its score and update the max score recursively.
                new_state: othello.State = current_state.applyMoveCloning(move)
                score: int = self.minimax(new_state, depth - 1, True)
                min_score = min(min_score, score)
            
            return min_score
    
    # Function that gets the Othello state, generates the available move and returns the best move using standard minimax algorithm.
    def choose_move(self, state: othello.State) -> othello.OthelloMove:
        best_score: int = -math.inf
        best_move: othello.OthelloMove = None

        moves: list = state.generateMoves()

        for move in moves:
            # Maximizer agent's turn. 
            # Apply each move and we pass max_turn as False to simulate the minimizing agent's (opponent) turn.
            move_score: int = self.minimax(state.applyMoveCloning(move), self.__depth - 1, False)
            
            if move_score > best_score:
                best_score = move_score
                best_move = move
            
        return best_move


class AlphaBeta(game.Player):
    pass