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

        if not moves:
            return None

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
                # Apply each move, get its score and update the min score recursively.
                new_state: othello.State = current_state.applyMoveCloning(move)
                score: int = self.minimax(new_state, depth - 1, True)
                min_score = min(min_score, score)
            
            return min_score
    
    # Function that gets the Othello state, generates the available move and returns the best move using standard minimax algorithm.
    def choose_move(self, state: othello.State) -> othello.OthelloMove:
        best_score: int = -math.inf
        best_move: othello.OthelloMove = None

        moves: list = state.generateMoves()

        if not moves:
            return None

        for move in moves:
            # Maximizer agent's turn. 
            # Apply each move and we pass max_turn as False to simulate the minimizing agent's (opponent) turn.
            move_score: int = self.minimax(state.applyMoveCloning(move), self.__depth - 1, False)
            
            if move_score > best_score:
                best_score = move_score
                best_move = move
            
        return best_move

# !!!!!! NEED TO DOCUMENT THE TIMING AGAINST STANDARD MINMAX FOR CODE DOCUMENTATION !!!!
class AlphaBeta(game.Player):
    def __init__(self, depth: int):
        super().__init__()
        self.__depth: int = depth

    # Function that uses alpha-beta pruning minimax algorithm to help choose our AI the best move. 
    # Evaluation function is the score.
    # We will use the tree with max as root as we want the move that gives the agent the max score.
    def alphaBetaPruning(self, current_state:othello.State, depth: int, alpha: int, beta: int, max_turn: bool) -> int:
        if current_state.game_over() or depth == 0:
            return current_state.score()
        
        moves: list = current_state.generateMoves()

        if max_turn:
            max_score: int = -math.inf

            for move in moves:
                # Apply each move, get its score and update the max score recursively.
                new_state: othello.State = current_state.applyMoveCloning(move)

                # We pass max_turn as False to simulate the minimizing agent's (opponent) turn.
                score: int = self.alphaBetaPruning(new_state, depth - 1, alpha, beta, False)
                max_score = max(max_score, score)
                alpha = max(alpha, score)

                # If this condition is true, then we don't need to waste time looking at other branches.
                if alpha >= beta:
                    break
            
            return max_score
        
        else:
            min_score: int = math.inf

            for move in moves:
                # Apply each move, get its score and update the min score recursively.
                new_state: othello.State = current_state.applyMoveCloning(move)

                # We pass max_turn as True to simulate the maximizing agent's (current_player) turn.
                score: int = self.alphaBetaPruning(new_state, depth - 1, alpha, beta, True)
                min_score = min(min_score, score)
                beta = min(beta, score)

                # If this condition is true, then we don't need to waste time looking at other branches.
                if alpha >= beta:
                    break
            
            return min_score


    def choose_move(self, state: othello.State) -> othello.OthelloMove:
        alpha: int = -math.inf
        beta: int = math.inf
        best_score: int = -math.inf
        best_move: othello.OthelloMove = None

        moves: list = state.generateMoves()

        if not moves:
            return None

        for move in moves:
            # Maximizer agent's turn. 
            # Apply each move and we pass max_turn as False to simulate the minimizing agent's (opponent) turn.
            move_score: int = self.alphaBetaPruning(state.applyMoveCloning(move), self.__depth - 1, alpha, beta, False)

            if move_score > best_score:
                best_score = move_score
                best_move = move
            
            alpha = max(alpha, move_score)
        
        return best_move
