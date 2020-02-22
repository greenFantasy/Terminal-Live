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
        self.enemy_health = []
        self.my_health = []




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

        self.enemy_health.append(game_state.enemy_health)
        self.my_health.append(game_state.my_health)

        Filter_Locations =  [[0, 13], [1, 13], [26, 13], [27, 13], [3, 12], [4, 12], [5, 12], [6, 12], [7, 12], [8, 12], [9, 12], [10, 12], [11, 12], [12, 12], [13, 12], [14, 12], [15, 12], [16, 12], [17, 12], [18, 12], [19, 12], [20, 12], [21, 12], [22, 12], [23, 12], [24, 12]]
        game_state.attempt_spawn(FILTER,Filter_Locations)
        Destructor_Locations = [[1, 12], [26, 12], [13, 8]]
        game_state.attempt_spawn(DESTRUCTOR,Destructor_Locations)
        deploy_locations =  [[3, 10], [24, 10]]
        ping_locations = [[4,10]]
        p = random.random()
        p = round(p)

        game_state.attempt_spawn(EMP, deploy_locations[p], int(game_state.get_resource(BITS)/game_state.type_cost(EMP)[1]))

        if (len(self.enemy_health) >= 2):

            if (self.enemy_health[len(self.enemy_health) - 1] - self.enemy_health[len(self.enemy_health) - 2] > 0):
                game_state.attempt_spawn(PING, ping_locations, int(game_state.get_resource(BITS)/game_state.type_cost(PING)[1]))

            elif (self.enemy_health[len(self.enemy_health) - 1] - self.enemy_health[len(self.enemy_health) - 2] < 0):
                game_state.attempt_spawn(SCRAMBLER, ping_locations, int(game_state.get_resource(BITS)/game_state.type_cost(SCRAMBLER)[1]))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
