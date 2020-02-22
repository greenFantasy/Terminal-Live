def find_units(game_state, name):
    mine, theirs = [], []
    map = game_state.game_map
    for loc in map:
        for unit in map[loc[0], loc[1]]:
            if unit.unit_type == name:
                if unit.player_index:
                    theirs.append(loc)
                else:
                    mine.append(loc)
    return mine, theirs
            
