import random
import sys


DEFAULT_STATE = '       | ###  -| # #  +| # ####|       '


class Action:

    def __init__(self, name, dx, dy):
        self.name = name
        self.dx = dx
        self.dy = dy


ACTIONS = [
    Action('UP', 0, -1),
    Action('RIGHT', +1, 0),
    Action('DOWN', 0, +1),
    Action('LEFT', -1, 0)
]


class State:

    def __init__(self, env, x, y):
        self.env: Env = env
        self.x: int = x
        self.y: int = y

    def clone(self) -> "State":
        return State(self.env, self.x, self.y)

    def is_legal(self, action) -> bool:
        cell = self.env.get(self.x + action.dx, self.y + action.dy)
        return cell is not None and cell in ' +-'
    
    def legal_actions(self, actions) -> list:
        legal = []
        for action in actions:
            if self.is_legal(action):
                legal.append(action)
        return legal
    
    def reward(self) -> int:
        cell = self.env.get(self.x, self.y)
        if cell is None:
            return 0
        elif cell == '+':
            return +10
        elif cell == '-':
            return -10
        else:
            return 0

    def at_end(self) -> bool:
        return self.reward() != 0

    def execute(self, action: Action):
        self.x += action.dx
        self.y += action.dy
        return self

    def __str__(self) -> str:
        tmp = self.env.get(self.x, self.y)
        self.env.put(self.x, self.y, 'A')
        s = ' ' + ('-' * self.env.x_size) + '\n'
        for y in range(self.env.y_size):
            s += '|' + ''.join(self.env.row(y)) + '|\n'
        s += ' ' + ('-' * self.env.x_size)
        self.env.put(self.x, self.y, tmp)
        return s


class Env:

    def __init__(self, string):
        self.grid = [list(line) for line in string.split('|')]
        self.x_size = len(self.grid[0])
        self.y_size = len(self.grid)

    def get(self, x: int, y: int) -> str:
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            return self.grid[y][x]
        else:
            return None

    def put(self, x: int, y: int, val: str):
        if x >= 0 and x < self.x_size and y >= 0 and y < self.y_size:
            self.grid[y][x] = val

    def row(self, y):
        return self.grid[y]

    def random_state(self) -> State:
        x = random.randrange(0, self.x_size)
        y = random.randrange(0, self.y_size)
        while self.get(x, y) != ' ':
            x = random.randrange(0, self.x_size)
            y = random.randrange(0, self.y_size)
        return State(self, x, y)


class QTable:

    def __init__(self, env: Env, actions: list):
        # initialize your q table
        self.__env: Env = env
        self.__actions: list[Action] = actions

        # A 3-D array q-table
        self.__qtable: list[list[list]] = [[[0.0 for action in self.__actions] for col in range(self.__env.x_size)] for row in range(self.__env.y_size)]

    def get_q(self, state: State, action: Action) -> float:
        # return the value of the q table for the given state, action
        action_index: int = 0

        for i in range(len(self.__actions)):
            if self.__actions[i].name == action.name:
                action_index = i
                break
        
        return self.__qtable[state.y][state.x][action_index]
        

    def get_q_row(self, state: State):
        # return the row of q table corresponding to the given state
        return self.__qtable[state.y][state.x]

    def set_q(self, state: State, action: Action, val: float) -> None:
        # set the value of the q table for the given state, action
        action_index: int = 0
        for i in range(len(self.__actions)):
            if self.__actions[i].name == action.name:
                action_index = i
                break
        
        self.__qtable[state.y][state.x][action_index] = val

    def learn_episode(self, alpha: float = 0.10, gamma: float = 0.90) -> None:
        # with the given alpha and gamma values,
        # from a random initial state,
        # consider a random legal action, execute that action,
        # compute the reward, and update the q table for (state, action).
        # repeat until an end state is reached (thus completing the episode)
        # also print the state after each action

        # Initial random state.
        current_state: State = self.__env.random_state()

        # Print the initial state.
        print(current_state)    # Uses _str_ method from the State class.

        # Loop until we reach at end.
        while not current_state.at_end():
            legal_actions: list[Action] = current_state.legal_actions(self.__actions)

            if not legal_actions:
                break
            
            # Choose a random action and execute it.
            random_action: Action = random.choice(legal_actions)
            previous_state: State = current_state.clone()
            current_state.execute(random_action)

            # Get the reward after executing the action.
            reward: int = current_state.reward()

            # Now, we will get the max q_value from this new state's q_row and update the previous state's q_value.
            q_row: list = self.get_q_row(current_state)
            max_q_value: float = 0.0
            
            for q_value in q_row:
                if q_value > max_q_value:
                    max_q_value = q_value
            
            previous_q_value: float = self.get_q(previous_state, random_action)

            # Use the Q-learning formula to update the q-value for previous state.
            # Q(𝑆,𝐴) ← (1−𝛼)𝑄(𝑆,𝐴) + 𝛼[𝑅 + 𝛾 max𝐴′𝑄(𝑆′, 𝐴′)]
            new_q_value: float = (1 - alpha) * previous_q_value + alpha * (reward + gamma * max_q_value)

            # Update the  q_value for the previous state.
            self.set_q(previous_state, random_action, new_q_value)

            # Print the new state.
            print(current_state)
                        
    def learn(self, episodes: int, alpha: float = 0.10, gamma: float = 0.90) -> None:
        # run <episodes> number of episodes for learning with the given alpha and gamma
        for i in range(episodes):
            self.learn_episode(alpha, gamma)

    def __str__(self) -> str:
        # return a string for the q table as described in the assignment
        q_table: str = ""

        for action_index in range(len(self.__actions)):
            current_action: Action = self.__actions[action_index]
            q_table += current_action.name + "\n"

            for row_index in range(self.__env.y_size):
                row: str = ""
                
                for column_index in range(self.__env.x_size):
                    current_q_value: float = self.__qtable[row_index][column_index][action_index]

                    if current_q_value == 0:
                        row += "----\t"
                    else:
                        row += f"{current_q_value:.2f}\t"

                q_table += row.rstrip() + "\n"
            q_table += "\n"
        
        return q_table


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        env = Env(sys.argv[2] if len(sys.argv) > 2 else DEFAULT_STATE)
        if cmd == 'learn':
            qt = QTable(env, ACTIONS)
            qt.learn(100)
            print(qt)
