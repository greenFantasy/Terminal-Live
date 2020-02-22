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
        dLocations = [[ 3, 12],[ 9, 12],[ 19, 12],[ 24, 12],[ 14, 9]]
        v1 = [[5, 13],[22, 13],[6, 12],[21, 12],[7, 11],[20, 11],[8, 10],[19, 10],[9, 9],[18, 9],[10, 8],[17, 8],[11, 7],[16, 7],[12, 6],[15, 6],[13, 5],[14, 5]]

        edges = [[0, 13],[ 27, 13],[ 1, 12],[ 26, 12],[ 2, 11],[ 25, 11],[ 3, 10],[ 24, 10],[ 4, 9],[ 23, 9],[ 5, 8],[ 22, 8],[ 6, 7],[ 21, 7],[ 7, 6],[ 20, 6],[ 8, 5],[ 19, 5],[ 9, 4],[ 18, 4],[ 10, 3],[ 17, 3],[ 11, 2],[ 16, 2],[ 12, 1],[ 15, 1],[ 13, 0],[ 14, 0]]

        random.shuffle(edges)

        game_state.attempt_spawn(DESTRUCTOR, dLocations)

        game_state.attempt_spawn(FILTER, v1)

        game_state.attempt_spawn(PING, edges)


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
