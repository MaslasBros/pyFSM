import sys
import os

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(src_dir)

from pyFsm.fsmLib import *

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
    fsm = FSM()
    fsm1 = FSM()
    fsm2 = FSM()
    fsm3 = FSM()

    #Multiple FSMs declaration
    print("FSM0 declarations")
    fsm.createTransition(idle, load, loading)
    fsm.printStates()
    fsm.printTransitions()
    fsm.printStatePairs()

    print("\nFSM2 declarations")
    fsm2.createTransition(aim, fire, aiming)
    #Tests on the same method in different FSMs assignement
    fsm2.createTransition(idle, load, loading)
    fsm2.createTransition(load, aim)

    fsm2.printStates()
    fsm2.printTransitions()
    fsm2.printStatePairs()

    #Piping and dynamic methods tests
    print("\nFSM piping and dynamic method calling")
    fsm.idle()
    fsm.load()

    fsm.idle().load()

    print("\nFSM2 piping and dynamic method calling")
    fsm2.aim()
    fsm2.fire()

    fsm2.aim().fire()
    pass

if __name__ == '__main__':
    _start_()
    pass