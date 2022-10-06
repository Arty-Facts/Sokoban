import state, utils, click
from heapq import heappop, heappush, heapify
from functools import total_ordering
import state_builder as sb
import numba

def player_input():
    print(
        "Press w:(up), a:(left), s:(down), d:(right), u(undo), h(help)"
        "\nPress b to go back to menu"
    )
    action = None
    while action not in ["w", "a", "s", "d", "b", "u", "h"]:
        action = click.getchar().lower()
    return action

def move(game_state, delta):
    player_pos = state.get_player(game_state)
    new_pos = next_pos(player_pos, delta)
    if state.is_at(game_state, new_pos, state.box()):
            next_box_pos = next_pos(new_pos, delta)
            if state.box_can_move(game_state, next_box_pos):
                state.move_box(game_state, new_pos, next_box_pos)
    if state.player_can_move(game_state, new_pos):
        state.move_player(game_state, player_pos, new_pos)

def undo(game_state):
    state.undo(game_state)

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

def unsavable(game, actions):
    level = game["active_level"]
    boxes = [k for k,v in level.items() if v == sb.box()]
    for bpos in boxes:
        for f, s in ["wd", "wa", "as", "sd"]:
            if state.is_at(game, next_pos(bpos, DELTA[f]), sb.wall())\
            and state.is_at(game, next_pos(bpos, DELTA[s]), sb.wall()):
                return True
         
        for w1, w2, b1 in ["aqw", "wed", "dcs", "sza", "azs", "scd", "dew", "wqa"]:
            if state.is_at(game, next_pos(bpos, DELTA[w1]), sb.wall())\
                and state.is_at(game, next_pos(bpos, DELTA[w2]), sb.wall())\
                and state.is_at(game, next_pos(bpos, DELTA[b1]), sb.box()):
                return True
    done = len([item for item in state.items(game) if item == sb.combine(sb.storage(),sb.box()) ])
    
    # if done > 0:
    #     print(done)
    #     print(state.active_game_to_dstr(game))
    # print((level["x"]+level["y"]), done, len(actions))
    if (level["x"]+level["y"]) * 1.3 * (done+1) < len(actions):
        return True   
    # else:
    
    return False

def score(game):
    level = game["active_level"]
    boxes = [k for k,v in level.items() if v == sb.box()]
    storages = [k for k,v in level.items() if v == sb.storage()]
    tot_dist = 0
    for bx, by in boxes:
        max_dist = 0
        for sx, sy in storages:
            dist = abs(bx - sx) + abs(by - sy)
            max_dist = max(max_dist, dist)
        tot_dist += max_dist
    return tot_dist
@total_ordering
class Wrapper:
    def __init__(self, game, game_state, actions):
        self.game_state, self.actions = game_state, actions
        self.score = score(game) + len(actions)
        # self.score = len(actions)
    def __lt__(self, other):
        return self.score < other.score
 
    def __eq__(self, other):
        return self.score == other.score
    
    def items(self):
        return self.score, self.game_state, self.actions

# @numba.jit(nopython=True)
def solve(game_state):
    root = state.active_game_to_dstr(game_state)
    visited = set()
    visited.add(root)
    front = []
    heapify(front)
    heappush(front, Wrapper(game_state, root, []))
    # front.append((root, []))
    ms = 0
    while len(front) > 0:
        s, curr, actions = heappop(front).items()
        # curr, actions = front.pop(0)
        al = len(actions)
        if ms < s:
            ms = s
            print(al, s-al, len(visited))
            print(curr)
        # print(actions)
        curr_game = {"running": True, "active_level": state.parse_level(curr)}
        if done(curr_game):
            print(actions)#lvl 1 231
            print(len(visited))
            return actions

        for action in "wasd":
            curr_game = {"running": True, "active_level": state.parse_level(curr)}
            move(curr_game, DELTA[action])
            next_state = state.active_game_to_dstr(curr_game)
            if next_state in visited:
                continue
            if unsavable(curr_game, actions):
                # print(al, s-al, len(actions))
                # print(next_state)
                # exit()
                continue
            visited.add(next_state)
            heappush(front, Wrapper(curr_game, next_state, actions + [action]))
            # front.append((next_state, actions + [action]))
    return None


DELTA = {
    "w" : (-1, 0),
    "a" : ( 0,-1),
    "s" : ( 1, 0),
    "d" : ( 0, 1),
    "q" : ( -1, -1),
    "e" : ( -1, 1),
    "c" : ( 1, 1),
    "z" : ( 1, -1),
}

def run(game_state):
    display(game_state)
    actions = []
    moves = 0
    while not done(game_state):
        action = player_input()
        if action == "b":
            return 
        elif action == "u":
            undo(game_state)
        elif action == "h":
            if len(actions) == 0:
                actions = solve(game_state)
            action = actions.pop(0)
            move(game_state, DELTA[action])
        else:
            move(game_state, DELTA[action]) 
        display(game_state)
        print("moves:", moves)
        moves += 1

if __name__ == "__main__":
    game_state = state.init()
    state.set_active_level(game_state, 0)
    run(game_state)