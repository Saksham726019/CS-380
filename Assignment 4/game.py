import othello
import agent
# import util


class Player:
    def choose_move(self, state: othello.State):
        raise NotImplementedError


class Game:
    def __init__(self, initial_state: othello.State, player1: Player, player2: Player):
        self.initial_state: othello.State = initial_state
        self.players: list = [player1, player2]

    def play(self):
        state: othello.State = self.initial_state.clone()
        states: list = [state]

        player_index = 0

        while not state.game_over():
            # Display the current state in the console:
            print("\nCurrent state, " + othello.PLAYER_NAMES[state.nextPlayerToMove] + " to move:")
            print(state)
            # Get the move from the player:
            player: Player = self.players[player_index]
            move = player.choose_move(state)

            if move != None: 
                print(move)

            state = state.applyMoveCloning(move)
            states.append(state)
            # util.pprint(state)
            player_index = (player_index + 1) % len(self.players)
        
        print("\n*** Final winner: " + state.winner() +" ***" )
        print(state)

        # If the player is minimax or alphabeta, print out the average time taken per move.
        # This proves that alphabeta is much faster.
        if isinstance(self.players[0], (agent.MinimaxAgent, agent.AlphaBeta)):
            self.players[0].printAverageTime()
        if isinstance(self.players[1], (agent.MinimaxAgent, agent.AlphaBeta)):
            self.players[1].printAverageTime()

        return states
