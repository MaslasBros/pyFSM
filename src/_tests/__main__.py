import sys
import os
from traceback import print_tb

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

def _start_():
    global toShoot 
    toShoot = 2 

    fsm = FSM(idle) # initial state of the FSM

    fsm.createTransition(idle, load, loading)
    fsm.createTransition(idle, release)
    fsm.createTransition(load, aim, aiming)
    fsm.createTransition(aim, fire)
    fsm.createTransition(fire, idle)

    fsm.onStateReached(callOnStateReached, callOnStateReached2)
    fsm.onDestinationReached(callOnDestReached, callOnDestReached2)

    """ for i in fsm._routes.items():
        print(i) """
    
    print("Current state {}".format(fsm.getCurrentFsmState()))
    fsm.fire(toShoot).idle().aim()

    print("Reseting FSM...")
    fsm.forceResetFSM()

    print("Current state {}".format(fsm.getCurrentFsmState()))

    pass

if __name__ == '__main__':
    _start_()
    pass