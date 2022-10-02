import state, utils

def parse(option, lvl_count):
    try:
        level = int(option)
        if abs(level) >= lvl_count:
            print(f"Level {level} does not exist!")
            return None
    except:
        print(f"{option} not allowd!")
        return None
    return level

def display(game_state, level):
    utils.clear()
    data = state.level_to_str(game_state, level)
    if data != None:
        print(data)
    else: 
        print(utils.Que)


def run(game_state):
    lvl_count = state.level_count(game_state)

    resume = ""
    if state.is_level_active(game_state):
        resume = "\nPress r to resume game"

    option = input(f"\n\nSelect a level 1-{lvl_count-1}"
                   f"{resume}"
                    "\nPress q to quit"
                    "\n:").lower()

    while option != "p":
        if option == "r":
            return 
        elif option == "q":
            state.end(game_state)
            return 

        level = parse(option, lvl_count)
        display(game_state, level)

        option = input(f"Level selected is {level}"
                       f"{resume}"
                        "\nPress p to play"
                        "\nPress q to quit"
                       f"\nOr select a new level 1-{lvl_count-1}"
                        "\n:").lower()

    state.set_active_level(game_state, level)

if __name__ == "__main__":
    game_state = state.init()
    run(game_state)
    state.game_over(game_state)