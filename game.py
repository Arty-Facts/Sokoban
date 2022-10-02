import state, utils, click

def player_input():
    print(
        "Press w:(up), a:(left), s:(down), d:(right)"
        "\nPress b to go back to menu"
    )
    action = None
    while action not in ["w", "a", "s", "d", "b"]:
        action = click.getchar().lower()
    return action

def move(game_state, delta):
    player_pos, player = state.get_player(game_state)
    new_pos = next_pos(player_pos, delta)
    if state.is_at(game_state, new_pos, state.box()):
            next_box_pos = next_pos(new_pos, delta)
            if state.box_can_move(game_state, next_box_pos):
                state.move_box(game_state, new_pos, next_box_pos)
    if state.player_can_move(game_state, new_pos):
        state.move_player(game_state, player_pos, new_pos)

def next_pos(pos, delta):
    px, py = pos
    dx, dy = delta
    return px+dx, py+dy

def done(game_state):
    if not state.is_level_active(game_state) or not state.is_game_running(game_state):
        return True
    for item in state.items(game_state):
        if item == state.box():
            return False
    state.disable_active_level(game_state)
    print(utils.ToGood)
    return True

def display(game_state):
    utils.clear()
    print(utils.Sokoban)
    print(state.active_game_to_str(game_state))

DELTA = {
    "w" : (-1, 0),
    "a" : ( 0,-1),
    "s" : ( 1, 0),
    "d" : ( 0, 1),
}

def run(game_state):
    display(game_state)
    while not done(game_state):
        action = player_input()
        if action == "b":
            return 
        move(game_state, DELTA[action]) 
        display(game_state)

if __name__ == "__main__":
    game_state = state.init()
    state.set_active_level(game_state, 0)
    run(game_state)