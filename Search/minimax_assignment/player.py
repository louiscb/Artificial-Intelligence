#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
import time
import sys


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


def evaluate_state(node):
    player1_score, player2_score = node.state.get_player_scores()
    player1_currently_caught_fish, player2_currently_caught_fish = node.state.get_caught()
    fish_scores = node.state.get_fish_scores()

    # add fish currently caught on hook to score of state
    if player1_currently_caught_fish is not None:
        player1_score += fish_scores[player1_currently_caught_fish]
    if player2_currently_caught_fish is not None:
        player2_score += fish_scores[player2_currently_caught_fish]

    return player1_score - player2_score


def sort_list(list_of_children, desc):
    if list_of_children is not None:
        list_of_children.sort(key=evaluate_state, reverse=desc)
    return list_of_children


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()
        self.start_time = None
        self.LENGTH_OF_TURN = .055

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate game tree object
        first_msg = self.receiver()
        # Initialize your minimax model
        model = self.initialize_model(initial_data=first_msg)

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(
                model=model, initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def initialize_model(self, initial_data):
        """
        Initialize your minimax model
        :param initial_data: Game data for initializing minimax model
        :type initial_data: dict
        :return: Minimax model
        :rtype: object

        Sample initial data:
        { 'fish0': {'score': 11, 'type': 3},
          'fish1': {'score': 2, 'type': 1},
          ...
          'fish5': {'score': -10, 'type': 4},
          'game_over': False }

        Please note that the number of fishes and their types is not fixed between test cases.
        """
        # EDIT THIS METHOD TO RETURN A MINIMAX MODEL ###
        return None

    def search_best_next_move(self, model, initial_tree_node):
        """
        Use your minimax model to find best possible next move for player 0 (green boat)
        :param model: Minimax model
        :type model: object
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE FROM MINIMAX MODEL ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!

        if self.should_pull_fish_up(initial_tree_node):
            return "up"

        self.start_time = time.time()
        winningest_node = self.iterative_deepening_search(initial_tree_node, 4)
        return ACTION_TO_STR[winningest_node.move]

    def iterative_deepening_search(self, initial_tree_node, initial_depth):
        winningest_node = None
        search_depth = initial_depth
        while True:
            try:
                winningest_node = self.minimax(initial_tree_node, 0, search_depth, float('-inf'), float('inf'))[0]
                search_depth += 1
            except:
                return winningest_node

    def should_pull_fish_up(self, initial_tree_node):
        if initial_tree_node.state.get_caught()[0] is None:
            return False
        fish_scores = initial_tree_node.state.get_fish_scores()
        fish_on_player1_hook = fish_scores[initial_tree_node.state.get_caught()[0]]
        return fish_on_player1_hook > 0

    def no_fish_left(self, state):
        return len(state.get_fish_positions()) == 0

    def run_out_of_time(self):
        if time.time() - self.start_time > self.LENGTH_OF_TURN:
            raise TimeoutError

    def minimax(self, node, player, depth, alpha, beta):
        self.run_out_of_time()
        # base case
        if depth == 0 or self.no_fish_left(node.state):
            return node, evaluate_state(node)

        if player == 0:
            best_possible = float('-inf')
            best_future_node = None
            for child_node in sort_list(node.compute_and_get_children(), True):
                best_node_in_child_subtree, value = self.minimax(child_node, 1, depth - 1, alpha, beta)
                if value > best_possible:
                    best_possible = value
                    best_future_node = child_node
                alpha = max(alpha, best_possible)
                if beta <= alpha:
                    break
            return best_future_node, best_possible

        else:
            worst_possible = float('inf')
            worst_future_node = None
            for child_node in sort_list(node.compute_and_get_children(), False):
                worst_node_in_child_subtree, value = self.minimax(child_node, 0, depth - 1, alpha, beta)
                if value < worst_possible:
                    worst_possible = value
                    worst_future_node = child_node
                beta = min(beta, worst_possible)
                if beta <= alpha:
                    break
            return worst_future_node, worst_possible
