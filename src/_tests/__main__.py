import sys
import os

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(src_dir)

from pyFsm.fsmLib import *

#The FSM transitions
@transition
def loading():
    print("Method loading")
    return True

@transition
def aiming():
    print("Method aiming")
    return True

# The FSM states
@state
def idle():
    print("Method idle")
    pass

@state
def fire():
    print("Method fire")
    pass

@state
def aim():
    print("Method aim")
    pass

@state
def load():
    print("Method load")
    pass

@state
def release():
    print("Method release")
    pass

def _start_():
    fsm = FSM(idle)

    fsm.createTransition(idle, load, loading)
    fsm.createTransition(idle, release)
    fsm.createTransition(load, aim, aiming)
    fsm.createTransition(aim, fire)
    fsm.createTransition(fire, idle)

    pass

if __name__ == '__main__':
    _start_()
    pass