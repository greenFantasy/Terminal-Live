from .game_state import DESTRUCTOR

def get_destructors(game_state):
    mine, theirs = [], []
    map = game_state.game_map
    for loc in map:
        for unit in map[loc[0], loc[1]]:
            if unit.unit_type == DESTRUCTOR:
                if unit.player_index:
                    theirs.append(loc)
                else:
                    mine.append(loc)
    return mine, theirs
            
