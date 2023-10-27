import sys
import os

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(src_dir)

from pyFsm.fsm import *

#The FSM transitions
@transition
def loading():
    print("Method loading")
    pass

@transition
def aiming():
    print("Method aiming")
    pass

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
    print("Saved states")
    printStates()
    print("\nSaved Transitions")
    printTransitions()

    pass

if __name__ == '__main__':
    _start_()
    pass