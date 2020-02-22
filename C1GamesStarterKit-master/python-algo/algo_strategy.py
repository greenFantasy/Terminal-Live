import gamelib
import random
import math
import warnings
from sys import maxsize
import json


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips:

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical
  board states. Though, we recommended making a copy of the map to preserve
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))
        self.turn_count = 0

    def on_game_start(self, config):
        """
        Read in config and perform any initial setup here
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER, BITS, CORES
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        BITS = 1
        CORES = 0
        # This is a good place to do initial setup
        self.scored_on_locations = []




    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """

        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        self.algo1(game_state)

        game_state.submit_turn()


    def algo1(self, game_state):

        self.turn_count += 1

        edge_one = [[ 0, 13],[ 1, 13],[ 2, 13],[ 3, 13],[ 6, 13],[ 7, 13],[ 8, 13],[ 9, 13],[ 10, 13],[ 11, 13],[ 12, 13],[ 13, 13],[ 14, 13],[ 15, 13],[ 16, 13],[ 17, 13],[ 18, 13],[ 19, 13],[ 20, 13],[ 21, 13],[ 22, 13],[ 23, 13],[ 24, 13],[ 25, 13],[ 26, 13],[ 27, 13],[ 1, 12]]

        destructor_one = [[2,12], [25,12], [7,12]]

        edge_two = [[4,12], [5,11], [6,10], [7,10], [8,10], [9,10], [26,12]]

        destructor_two = [[9,12]]

        edge_three = [[ 0, 13],[ 1, 13],[ 2, 13],[ 3, 13],[ 6, 13],[ 7, 13],[ 8, 13],[ 9, 13],[ 10, 13],[ 11, 13],[ 12, 13],[ 13, 13],[ 14, 13],[ 15, 13],[ 16, 13],[ 17, 13],[ 18, 13],[ 19, 13],[ 20, 13],[ 21, 13],[ 22, 13],[ 23, 13],[ 24, 13],[ 25, 13],[ 26, 13],[ 27, 13],[ 1, 12],[ 4, 12],[ 26, 12],[ 5, 11],[ 6, 10],[ 7, 10],[ 8, 10],[ 9, 10],[ 10, 10],[ 11, 10],[ 12, 10],[ 13, 10],[ 14, 10],[ 15, 10],[ 16, 10],[ 17, 10],[ 18, 10],[ 19, 10],[ 20, 10],[ 21, 10]]

        destructor_three = [[11,12], [13,12], [15,12], [17, 12], [19, 12]]

        edge_four = [[8,12], [10,12], [12,12], [14,12], [16,12], [18,12], [20,12]]

        

        game_state.attempt_spawn(DESTRUCTOR, destructor_one)
        game_state.attempt_spawn(FILTER, edge_one)
        game_state.attempt_spawn(FILTER, edge_two)
        game_state.attempt_spawn(DESTRUCTOR, destructor_two)
        game_state.attempt_spawn(FILTER, edge_three)
        game_state.attempt_spawn(DESTRUCTOR, destructor_three)

        game_state.attempt_spawn(EMP, [[24,10]])
        if self.turn_count % 3 == 0:
            for x in range(10):
                game_state.attempt_spawn(PING, [[12,1]])
                game_state.attempt_spawn(PING, [[15,1]])



if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
