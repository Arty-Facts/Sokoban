import state, menu, game, utils

def game_over():
    print(utils.GameOver)

def main():
    game_state = state.init()
    while state.is_game_running(game_state):
        menu.run(game_state)
        game.run(game_state)
    game_over()

if __name__ == "__main__":
    main()