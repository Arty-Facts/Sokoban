from pathlib import Path
from utils import *
import state_builder as sb


def create_level():
    return {"history":[]}

def can_move(state, pos, item):
    level = state["active_level"]
    return sb.valid(sb.combine(get(level, pos), item))

def player_can_move(state, pos):
    return can_move(state, pos, sb.player())

def box_can_move(state, pos):
    return can_move(state, pos, sb.box())

def move(level, src, dest, item):
    history = []
    if sb.remove(level, src, item):
        history.append(lambda: sb.add(level, src, item))
    else:
        return False

    if sb.add(level, dest, item):
        history.append(lambda: sb.remove(level, dest, item))
    else:
        history[0]()
        return False
    level["history"].append(history)
    return True

def undo(state):
    level = state["active_level"]
    history = level["history"]
    if len(history) != 0:
        actions = history.pop(-1)
        for a in actions:
            a()

def move_player(state, src, dest):
    level = state["active_level"]
    return move(level, src, dest, sb.player())

def move_box(state, src, dest):
    level = state["active_level"]
    return move(level, src, dest, sb.box())

def box():
    return sb.box()

def get(level, pos):
    if pos in level:
        return level[pos]
    return sb.ID["floor"]

def get_tile(state, pos):
    return get(state["active_level"], pos)

def get_player(state):
    if state["active_level"] == None:
        return None
    for pos in filter(lambda x:x != "history" ,state["active_level"]):
        if sb.at(state["active_level"], pos, sb.player()):
            return pos

def is_at(state, pos, id):
    if state["active_level"] == None:
        return False
    return sb.at(state["active_level"], pos, id)
    
def to_str(level):
    if level == None:
        return ""
    res = []
    for x in range(level["x"]):
        for y in range(level["y"]):
            res.append(sb.ID_TO_STR[get(level, (x,y))])
        res.append("\n")
    res.append("\n")
    return "".join(res)
    

def active_game_to_str(state):
    return to_str(state["active_level"])

def level_to_str(state, lvl):
    if lvl != None:
        return to_str(state["levals"][lvl])
    else:
        return None

def items(state):
    if state["active_level"] == None:
        return []
    return (id for _pos, id in state["active_level"].items())

def disable_active_level(state):
    state["active_level"] == None

def parse_level(level_data):
    level = create_level()
    max_x = 0
    max_y = 0
    for x, line in enumerate(level_data.split("\n")):
        max_x = max(max_x, x)
        for y, item in enumerate(line):
            max_y = max(max_y, y)
            if   "@" == item:
                sb.add_player(level, (x, y))
            elif "#" == item:
                sb.add_wall(level, (x, y))
            elif "o" == item:
                sb.add_box(level, (x, y))
            elif "." == item:
                sb.add_storage(level, (x, y))
            elif "+" == item:
                sb.add_player(level, (x, y))
                sb.add_storage(level, (x, y))
            elif "*" == item:
                sb.add_box(level, (x, y))
                sb.add_storage(level, (x, y))
    level["x"] = max_x + 1
    level["y"] = max_y + 1
    return level 

def parse_levels(levels_data):
    levels = []
    for level_data in levels_data.split("\n\n"):
        level = parse_level(level_data)
        levels.append(level)
    return levels

def is_game_running(state):
    return state["running"]

def end(state):
    state["running"] = False

def level_count(state):
    return len(state["levals"])

def set_active_level(state, lvl):
    if lvl != None:
        state["active_level"] = state["levals"][lvl].copy()

def active_game(state):
    return state["active_level"]

def is_level_active(state):
    return active_game(state) != None

def init():
    clear()
    print(WelcomeTo+Sokoban)
    state = {
        "running": True,
        "levals" : [],
        "active_level" : None,
        "level_file" : "sokoban_levels.txt"
    }
    file_content = Path(state["level_file"]).read_text()
    state["levals"] = parse_levels(file_content)
    return state

if __name__ == "__main__":
    state = init()
    print(to_str(state["levals"][1]))
