import sys
import os

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(src_dir)

from pyFsm import *
from time import sleep

#The FSM transitions
@transition
def loading():
    print("Loading...")
    sleep(1)
    pass

@transition
def aiming():
    print("Aiming...")
    sleep(2)
    pass

# The FSM states
@state
def idle():
    print("Idling...")
    pass

@state
def fire(shots):
    print("{} Shots fired!".format(shots))
    pass

@state
def aim():
    print("Aimed.")
    pass

@state
def load():
    print("Loaded")
    pass

@state
def release():
    print("Released")
    pass

def callOnStateReached():
    print("Reached a state")
    pass

def callOnStateReached2():
    print("Reached a state 2")
    pass

def callOnDestReached():
    print("Reached the destination")
    pass

def callOnDestReached2():
    print("Reached the destination2")
    pass

#Merparser Test
_stateDiagramTest = """
        ---
        title: Simple sample
        ---
        stateDiagram-v2
            idle --> load: "loading"
            idle --> release
            load --> aim: "aiming"
            aim --> fire
            fire --> idle
        """

def _start_():
    global toShoot 
    toShoot = 2 

    fsm = FSM(idle)
    fsm.createTransitionsFromDiagram(_stateDiagramTest)

    fsm.fire(toShoot).idle().aim().fire(5).idle()
    pass

if __name__ == '__main__':
    _start_()
    pass