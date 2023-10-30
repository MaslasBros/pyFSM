import sys
import os

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(src_dir)

from pyFsm.fsmLib import *

fsm = FSM()

#The FSM transitions
@fsm.transition
def loading():
    print("Method loading")
    pass

@fsm.transition
def aiming():
    print("Method aiming")
    pass

# The FSM states
@fsm.state
def idle():
    print("Method idle")
    pass

@fsm.state
def fire():
    print("Method fire")
    pass

@fsm.state
def aim():
    print("Method aim")
    pass

@fsm.state
def load():
    print("Method load")
    pass

@fsm.state
def release():
    print("Method release")
    pass

def _start_(fsm:FSM):
    print("Saved states")
    fsm.printStates()
    print("\nSaved Transitions")
    fsm.printTransitions()

    fsm.createTransition(idle, load, loading)
    fsm.createTransition(idle, release)
    fsm.createTransition(load, aim, aiming)
    fsm.createTransition(aim, fire)
    fsm.createTransition(fire, idle)

    print("\nSaved State pairs")
    fsm.printStatePairs()

    fsm.load().fire()

    pass

if __name__ == '__main__':
    _start_(fsm)
    pass