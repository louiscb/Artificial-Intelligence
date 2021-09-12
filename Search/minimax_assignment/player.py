#!/usr/bin/env python3
import random

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR
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


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

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

        winningest_node = self.minimax(initial_tree_node, 0, 3)
        next_node = self.traverse_up_the_tree(initial_tree_node, winningest_node)
        return ACTION_TO_STR[next_node.move]

    def traverse_up_the_tree(self, end_node, start_node):
        current_node = start_node
        while current_node.parent != end_node:
            current_node = current_node.parent
            if current_node.depth == 0:
                return None
        return current_node

    def heuristic(self, state):
        player1_score, player2_score = state.get_player_scores()
        return player1_score - player2_score

    def minimax(self, node, player, depth):
#        print(depth)
#        if node.move != None:
#            print(ACTION_TO_STR[node.move])

        if depth == 0:  # or if game is over, how do we know if game is over?
            return node

        if player == 0:
            best_possible = float('-inf')
            best_future_node = None
            for child_node in node.compute_and_get_children():
                best_node_in_child_subtree = self.minimax(child_node, 1, depth - 1)
                value = self.heuristic(best_node_in_child_subtree.state)
                if value > best_possible:
                    best_possible = value
                    best_future_node = best_node_in_child_subtree
            return best_future_node

        else:
            best_possible = float('inf')
            best_future_node = None
            for child_node in node.compute_and_get_children():
                best_node_in_child_subtree = self.minimax(child_node, 0, depth - 1)
                value = self.heuristic(best_node_in_child_subtree.state)
                if value < best_possible:
                    best_possible = value
                    best_future_node = best_node_in_child_subtree
            return best_future_node
