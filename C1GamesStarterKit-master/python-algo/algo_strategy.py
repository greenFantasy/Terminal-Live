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
        self.my_health = []
        self.defense_action = []
        self.offense_action = []
        self.edges = [[0,13],[27,13],[1,12],[26,12],[2,11],[25,11],[3,10],[24,10],[4,9],[23,9],[5,8],[22,8],[6,7],[21,7],[7,6],[20,6],[8,5],[19,5],[9,4],[18,4],[10,3],[17,3],[11,2],[16,2],[12,1],[15,1],[13, 0],[14, 0]]
        self.bottom_edges = [e for e in self.edges if e[1] < 4]
        self.top_edges = [e for e in self.edges if e[1] > 10]
        self.defended = True
        self.breaches = {str(edge): 0 for edge in self.edges}
        self.enemy_health = 0
        self.enemy_damage = 0
        self.myDestructors = []
        self.theirDestructors = []

    def on_action_frame(self, turn_string):
        state = json.loads(turn_string)
        breaches = state['events']['breach']
        for breach in breaches:
            if breach[4] != 1:
                self.breaches[str(breach[0])] += 1


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
        self.myDestructors, self.theirDestructors = gamelib.find_units(game_state, DESTRUCTOR)
        self.enemy_damage = self.enemy_health - game_state.enemy_health
        self.enemy_health = game_state.enemy_health

        self.algo1(game_state)

        game_state.submit_turn()


    def algo1(self, game_state):
        self.my_health.append(game_state.my_health)
        self.attack(game_state)
        # DEFENSE SEQUENCE
        for i in range(1):
            if (not self.filters1(game_state)):
                break
            if (not self.destructors1(game_state)):
                break
            self.upgradeFilters1(game_state)
            if (not self.destructors2(game_state)):
                break
            if (not self.encryptors1(game_state)):
                break
            if (not self.destructors3(game_state)):
                break
            self.upgradeFilters2(game_state)
            if (not self.encryptors2(game_state)):
                break
            self.freeCores(game_state)

    def attack(self,game_state):
        nums = self.getNumber(game_state)
        gamelib.debug_write('nums: {}'.format(nums))
        weakSide = self.weakSide()
        self.deployEMP(game_state,weakSide,nums[0])
        self.deployScrambler(game_state, nums[1])
        self.deployPing(game_state,nums[2])

    def getNumber(self,game_state):
        # return number of stuff we want to deploy this turn
        nums = [0,0,0]
        leftRegion = [[9, 23], [8, 22], [9, 22], [7, 21], [8, 21], [9, 21], [6, 20], [7, 20], [8, 20], [9, 20], [5, 19], [6, 19], [7, 19], [8, 19], [9, 19], [4, 18], [5, 18], [6, 18], [7, 18], [8, 18], [9, 18], [3, 17], [4, 17], [5, 17], [6, 17], [7, 17], [8, 17], [9, 17], [2, 16], [3, 16], [4, 16], [5, 16], [6, 16], [7, 16], [8, 16], [9, 16], [1, 15], [2, 15], [3, 15], [4, 15], [5, 15], [6, 15], [7, 15], [8, 15], [9, 15], [0, 14], [1, 14], [2, 14], [3, 14], [4, 14], [5, 14], [6, 14], [7, 14], [8, 14], [9, 14]]
        rightRegion = [[19, 22], [19, 21], [20, 21], [19, 20], [20, 20], [21, 20], [19, 19], [20, 19], [21, 19], [22, 19], [19, 18], [20, 18], [21, 18], [22, 18], [23, 18], [19, 17], [20, 17], [21, 17], [22, 17], [23, 17], [24, 17], [19, 16], [20, 16], [21, 16], [22, 16], [23, 16], [24, 16], [25, 16], [19, 15], [20, 15], [21, 15], [22, 15], [23, 15], [24, 15], [25, 15], [26, 15], [19, 14], [20, 14], [21, 14], [22, 14], [23, 14], [24, 14], [25, 14], [26, 14], [27, 14]]
        OpponentBits = game_state.get_resource(BITS,1)
        if(OpponentBits>=10 and OpponentBits < 14):
            nums[1] = 1
        elif(OpponentBits>= 14 and OpponentBits < 20):
            nums[1] = 2
        elif(OpponentBits >= 20):
            nums[1] = 3
        else:
            nums[1] = 0
        remainingBITS = game_state.get_resource(BITS,0) - nums[1]
        gamelib.debug_write('{}'.format(remainingBITS))
        if(gamelib.unit_sector(game_state, DESTRUCTOR, leftRegion) or gamelib.unit_sector(game_state,DESTRUCTOR,rightRegion) and game_state.turn_number >= 10):
            nums[2] = int(math.floor(0.2*remainingBITS))
            if(nums[2]<0):
                nums[2] = 0
        else:
            nums[2] = 0
        remainingBITS = remainingBITS - nums[2]
        gamelib.debug_write('{}'.format(remainingBITS))
        nums[0] = int(math.floor(remainingBITS/3))
        return nums

    def deployEMP(self,game_state,weakSide,num):
        if(not weakSide):
            rightProb = [0.5,0.2,0.2,0.1]
            rightEMPLocations = [[3, 10], [4, 9], [5, 8], [6, 7]]
            deployIndex = 0
            p = random.random()
            if(p < rightProb[0]):
                deployIndex = rightEMPLocations[0]
            elif(p > rightProb[0] and p< rightProb[0]+rightProb[1]):
                deployIndex = rightEMPLocations[1]
            elif(p > rightProb[0]+rightProb[1] and p < rightProb[0]+rightProb[1]+rightProb[2]):
                deployIndex = rightEMPLocations[2]
            else:
                deployIndex = rightEMPLocations[3]
            game_state.attempt_spawn(EMP, deployIndex, num)
        else:
            leftEMPLocation = [[18, 4]]
            game_state.attempt_spawn(EMP,leftEMPLocation,num)

    def deployScrambler(self,game_state,num):
        location = [[7, 6], [20, 6]]
        p = random.random()
        p = round(p)
        if(num == 1):
            game_state.attempt_spawn(SCRAMBLER,location[p],1)
        elif(num == 2):
            game_state.attempt_spawn(SCRAMBLER,location,1)
        elif(num == 3):
            game_state.attempt_spawn(SCRAMBLER,location[p],2)
            game_state.attempt_spawn(SCRAMBLER,location[1-p],1)

    def deployPing(self,game_state,num):
        location = [[9, 4]]
        game_state.attempt_spawn(PING,location,num)

    def weakSide(self):
        x = 0
        if(len(self.theirDestructors) != 0 ):
            for i in range(0,len(self.theirDestructors)):
                x = x + self.theirDestructors[i][0]
            x = x/len(self.theirDestructors)
            if(x <= 13):
                return True
            return False
        return False

    def filters1(self, game_state):
        fLocations = [[0, 13], [27, 13], [1, 12], [2, 12], [3, 12], [4, 12], [5, 12], [6, 12], [7, 12], [8, 12], [9, 12], [10, 12], [11, 12], [12, 12], [13, 12], [14, 12], [15, 12], [16, 12], [17, 12], [18, 12], [19, 12], [23, 12], [24, 12], [25, 12], [26, 12]]
        return self.genericDefenseCall(game_state, FILTER, fLocations)

    def destructors1(self, game_state):
        dLocations = [[5,11],[11,11],[19,11],[23,11]]
        return self.genericDefenseCall(game_state, DESTRUCTOR, dLocations)

    def upgradeFilters1(self, game_state):
        fLocations = [[0,13],[1,12],[2,12],[3,12],[10,12],[11,12],[12,12]]
        game_state.attempt_upgrade(fLocations)

    def destructors2(self, game_state):
        dLocations = [[18,11],[19,10],[23,10]]
        return self.genericDefenseCall(game_state, DESTRUCTOR, dLocations)

    def encryptors1(self, game_state):
        eLocations = [[17,8],[18,8],[17,7]]
        return self.genericDefenseCall(game_state, ENCRYPTOR, eLocations)

    def destructors3(self, game_state):
        dLocations = [[8,11],[13,11]]
        return self.genericDefenseCall(game_state, DESTRUCTOR, dLocations)

    def upgradeFilters2(self, game_state):
        fLocations = [[17,12],[27,13]]
        game_state.attempt_upgrade(fLocations)

    def encryptors2(self, game_state):
        eLocations = [[16,7],[18,7],[17,6],[16,8],[16,6],[18,6]]
        return self.genericDefenseCall(game_state, ENCRYPTOR, eLocations)

    def freeCores(self, game_state):
        dLocations = [[2, 11], [3, 11], [4, 11], [5, 11], [6, 11], [7, 11], [8, 11], [9, 11], [10, 11], [11, 11], [12, 11], [13, 11], [14, 11], [15, 11], [16, 11], [17, 11], [18, 11], [19, 11], [20, 11], [19, 10], [18, 9], [17, 8]]
        self.genericDefenseCall(game_state, DESTRUCTOR, dLocations)

    def upgradeEncryptors(self, game_state):
        for x in range(28):
            for y in range(14):
                if (game_state.game_map[x,y].unit_type == ENCRYPTOR):
                    game_state.attempt_upgrade([x,y])

    def checkPlaced(self, game_state, locations):
        for p in locations:
            if (not game_state.contains_stationary_unit(p)):
                return False
        return True

    def genericDefenseCall(self, game_state, type, locations):
        if (not self.checkPlaced(game_state, locations)):
            self.smart_place(game_state, type, locations)
            return self.checkPlaced(game_state, locations)
        return True

    def smart_place(self, game_state, type, locations, min_cores = 0):
        i = 0
        while (game_state.get_resource(CORES, 0) > min_cores and i < len(locations)):
            game_state.attempt_spawn(type, locations[i])
            i += 1
        return i


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
