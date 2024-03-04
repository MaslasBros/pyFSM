from pyfsm.fsmLib import *
from pyfsm.fsmGlobals import *
from time import sleep

myFsm = None

#The FSM transitions
@transition
def loading():
    print("Loading...")
    sleep(1)
    pass

@transition
def aiming():
    print("Aiming...")
    i = 0
    while i <= 3:
        print(i)
        i+=1
        sleep(1)
        
    pass

# The FSM states
@state
def idle():
    print("Idling...")
    pass

@state(True)
def fire(shots):
    print("{} Shots fired!".format(shots))
    myFsm.nextState()
    pass

@state
def aim():   
    print("Aimed.")
    pass

@state(True)
def load():
    print("Loaded")
    myFsm.nextState()
    pass

@state
def release():
    print("Released")
    pass

#Callbacks
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
    toShoot = 5

    global myFsm 
    myFsm = FSM(idle)

    myFsm.createTransition(idle, load, loading)
    myFsm.createTransition(load, aim, aiming)
    myFsm.createTransition(aim, fire)
    myFsm.createTransition(fire, idle)

    #Simulating of the callback from an external call
    myFsm.fire(toShoot).idle().fire(17).aim().idle()

    myFsm.run()

    print("YES!")

    pass

if __name__ == '__main__':
    _start_()
    pass