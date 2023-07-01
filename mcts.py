import math
import random

class MonteCarloTreeSearch:
    def __init__(self, game, num_iterations, save_data = False):
        self.game = game
        self.num_iterations = num_iterations
        self.save_data = save_data
        if self.save_data:
            self.data = {}

    def search(self, state, verbose = False):
        starting_state = state

        if self.save_data:
            data = self.data
        else:
            data = {}

        for _ in range(self.num_iterations):
            visited_actions = set()
            state = starting_state

            # Selection
            # traverse the tree, choosing child node with highest UCB1 score,
            # until we reach a leaf node or a node with untried actions
            if verbose: print("Selection step...")
            while True:
                if verbose: print(f"State: {state}")
                if self.game.is_game_over(state):
                    break
                legal_actions = self.game.get_legal_actions(state)
                if legal_actions and all(data.get((state, action)) for action in legal_actions):
                    best_action = self.select_ucb1_action(data, state, legal_actions)
                    visited_actions.add((state, best_action))
                    if state == (1, (2, 2, 1, 2, 1, 1, 1, 1, 2)):
                        print("(1, (2, 2, 1, 2, 1, 1, 1, 1, 2)) added in selection step")
                    state = self.game.get_next_state(state, best_action)
                else:
                    break
            if verbose: print("---")


            # Expansion
            # if we have untried actions, expand the tree by adding a new child node
            if verbose: print("Expansion step...")
            legal_actions = self.game.get_legal_actions(state)
            if legal_actions and not all(data.get((state, action)) for action in legal_actions):
                random_action = random.choice(legal_actions)
                visited_actions.add((state, random_action))
                if state == (1, (2, 2, 1, 2, 1, 1, 1, 1, 2)):
                    print("(1, (2, 2, 1, 2, 1, 1, 1, 1, 2)) added in expansion step")
                if verbose: print("(state, action):", (state, random_action))
                state = self.game.get_next_state(state, random_action)
            if verbose: print("---")

            # Simulation
            if verbose: print("Simulation step...")
            while not self.game.is_game_over(state):
                legal_actions = self.game.get_legal_actions(state)
                action = random.choice(legal_actions)
                state = self.game.get_next_state(state, action)
            
            winner = self.game.get_winner(state)
            if verbose: print(f"Winner: {winner}")
            if verbose: print("---")

            # Backpropagation
            if verbose: print("Backpropagation step...")
            for state, action in visited_actions:
                if (state, action) not in data:
                    data[(state, action)] = (0, 0)
                node = data[(state, action)]
                player = self.game.get_player(state)
                if player == winner:
                    new_node = (node[0] + 1, node[1] + 1)
                else:
                    new_node = (node[0] + 1, node[1])
                data[(state, action)] = new_node
            if verbose: print("---")

            if verbose:
                print("Data")
                for key, value in data.items():
                    print(key, value)
                print("---")

        state = starting_state
        legal_actions = self.game.get_legal_actions(state)
        if not all(data.get((state, action)) for action in legal_actions):
            print("Choosing randomly...")
            return_action = random.choice(legal_actions)
        else:
            return_action = self.select_best_action(data, starting_state, legal_actions, True)
        return return_action
    
    def select_ucb1_action(self, data, state, legal_actions, verbose = False):
        log_total_plays = math.log(sum(data[(state, action)][0] for action in legal_actions))
        best_action = None
        best_score = -math.inf
        for action in legal_actions:
            node = data[(state, action)]
            plays = node[0]
            wins = node[1]
            score = wins / plays + 1.4 * math.sqrt(log_total_plays / plays)
            if verbose: print(f"action: {action}, plays: {plays}, wins: {wins}, score: {score}")
            if score > best_score:
                best_action = action
                best_score = score
        if verbose: print("best action:", best_action)

        return best_action
    
    def select_best_action(self, data, state, legal_actions, verbose = False):
        best_action = None
        best_score = -math.inf
        for action in legal_actions:
            node = data[(state, action)]
            plays = node[0]
            wins = node[1]
            score = wins / plays
            if verbose: print(f"action: {action}, plays: {plays}, wins: {wins}, score: {score}")
            if score > best_score:
                best_action = action
                best_score = score
        if verbose: print("best action:", best_action)

        return best_action
    
    def get_data(self):
        return self.data
