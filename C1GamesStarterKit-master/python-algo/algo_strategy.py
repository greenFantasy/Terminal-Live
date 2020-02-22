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
        self.defense_action = []
        self.offense_action = []
        self.edges = [[0,13],[27,13],[1,12],[26,12],[2,11],[25,11],[3,10],[24,10],[4,9],[23,9],[5,8],[22,8],[6,7],[21,7],[7,6],[20,6],[8,5],[19,5],[9,4],[18,4],[10,3],[17,3],[11,2],[16,2],[12,1],[15,1],[13, 0],[14, 0]]
        self.bottom_edges = [e for e in self.edges if e[1] < 4]
        self.top_edges = [e for e in self.edges if e[1] > 10]
        self.defended = True




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
        mine, theirs = get_destructors(game_state)
        gamelib.debug_write("My destructors:" + str(mine))
        gamelib.debug_write("Their destructors:" + str(theirs))

        self.algo1(game_state)

        game_state.submit_turn()


    def algo1(self, game_state):
        self.enemy_health.append(game_state.enemy_health)
        self.my_health.append(game_state.my_health)
        # Actual Actions
        self.protect(game_state)
        self.deployDefenseInfrastracture(game_state)
        self.deployEMP(game_state)
        self.deployPingOrScrambler(game_state)


    def deployDefenseInfrastracture(self,game_state):
        Filter_Locations =  [[0, 13], [1, 13], [26, 13], [27, 13], [3, 12], [4, 12], [5, 12], [6, 12], [7, 12], [8, 12], [9, 12], [10, 12], [11, 12], [12, 12], [13, 12], [14, 12], [15, 12], [16, 12], [17, 12], [18, 12], [19, 12], [20, 12], [21, 12], [22, 12], [23, 12], [24, 12]]
        game_state.attempt_spawn(FILTER,Filter_Locations)
        Destructor_Locations = [[1, 12], [26, 12], [13, 8]]
        game_state.attempt_spawn(DESTRUCTOR,Destructor_Locations)

    def deployEMP(self,game_state):
        # Generate Deploy Location for EMP
        p = random.random()
        p = round(p)
        deploy_locations =  [[3, 10], [24, 10]]
        numOfEMP = int(game_state.get_resource(BITS)/game_state.type_cost(EMP)[1])
        game_state.attempt_spawn(EMP, deploy_locations[p], EMP)

    def deployPingOrScrambler(self,game_state):
        ping_locations = [[4,10]]
        if (len(self.enemy_health) >= 2):
            # If Our Attack From Last Trun works, Then There Is A Side Without Destructor
            if (self.enemy_health[len(self.enemy_health) - 1] - self.enemy_health[len(self.enemy_health) - 2] > 0):
                game_state.attempt_spawn(PING, ping_locations, int(game_state.get_resource(BITS)/game_state.type_cost(PING)[1]))
                # If We Are Losing Health
            elif (self.enemy_health[len(self.enemy_health) - 1] - self.enemy_health[len(self.enemy_health) - 2] < 0):
                game_state.attempt_spawn(SCRAMBLER, ping_locations, int(game_state.get_resource(BITS)/game_state.type_cost(SCRAMBLER)[1]))

    def protect(self, game_state):
    # DEPLOYING SCRAMBLERS WHICH PROTECT FROM ENEMY ATTACK
    if (game_state.get_resource(BITS, 1) > 7 or not defended):
        game_state.attempt_spawn(SCRAMBLER, [[5,8],[22,8],[9,4],[18,4]])

if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
