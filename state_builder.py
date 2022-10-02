from utils import *

ID = {
    "floor"  : 1,
    "wall"   : 2,
    "box"    : 3,
    "storage": 5,
    "player" : 7,
}
def combine(state, other):
    return state * other

def split(state, other):
    return state / other

ID_TO_STR = {
    ID["floor"]             : " ",
    ID["wall"]              : GELLOW+"#"+ENDC,
    ID["box"]               : RED+"o"+ENDC,
    ID["player"]            : GREEN+"@"+ENDC,
    ID["storage"]           : CYAN+"."+ENDC,
    combine(ID["box"], 
            ID["storage"])  : BLUE+"*"+ENDC,
    combine(ID["player"], 
            ID["storage"])  : GREEN+"+"+ENDC,
}

ID_TO_DSTR = {
    ID["floor"]             : " ",
    ID["wall"]              : "#",
    ID["box"]               : "o",
    ID["player"]            : "@",
    ID["storage"]           : ".",
    combine(ID["box"], 
            ID["storage"])  : "*",
    combine(ID["player"], 
            ID["storage"])  : "+",
}

VALID = [
    ID["floor"],
    ID["wall"],
    ID["box"],
    ID["storage"],
    ID["player"],
    combine(ID["box"], ID["storage"]),
    combine(ID["player"], ID["storage"]),
]

def box():
    return ID["box"]

def wall():
    return ID["wall"]

def player():
    return ID["player"]

def storage():
    return ID["storage"]

def valid(item):
    return item in VALID

def at(level, pos, item):
    if pos not in level:
        return False
    return level[pos] % item == 0

def remove(level, pos, item):
    if not at(level, pos, item):
        return False 

    level[pos] = split(level[pos], item) 
    if level[pos] == ID["floor"]:
        level.pop(pos)
    return True

def add(level, pos, item):
    if pos in level:
        level[pos] = combine(level[pos] ,item)
    else:
        level[pos] = item
    return True

def add_wall(level, pos):
    return add(level, pos, ID["wall"])

def add_box(level, pos):
    return add(level, pos, ID["box"])

def add_player(level, pos):
    return add(level, pos, ID["player"])

def add_storage(level, pos):
    return add(level, pos, ID["storage"])

def remove_wall(level, pos):
    return remove(level, pos, ID["wall"])

def remove_box(level, pos):
    return remove(level, pos, ID["box"])

def remove_player(level, pos):
    return remove(level, pos, ID["player"])

def remove_storage(level, pos):
    return remove(level, pos, ID["storage"])
