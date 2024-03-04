# Python FSM implementation

## Table of Contents

- [Description](#description)
- [Syntax](#syntax)
  - [States and Transitions](#states-and-transitions)
  - [Events](#events)
  - [FSM Creation](#fsm-creation)
- [Compatibility](#compatibility)
- [Dependencies](#dependencies)

## Description

An FSM(Finite State Machine) is a an old and extensively used in industrial automation method of switching the current state of a machine to another connected state by forcing it to transition by a predetermined path until it reaches its target.

## Syntax

### States and Transitions
A typical FSM consists of:
- States
- Transitions

In the pyFsm module states and transitions are decorated methods, as such...
```python
from pyfsm.fsmLib import *
from pyfsm.fsmGlobals import *

@state
def a_state():
  # magical stuff
  pass

@transition
def a_transition():
  # magical stuff
  pass
```

...if a True boolean argument is passed in the **state** decorator then the FSM will wait on that state for the fsm.nextState() to get called instead of continuing on to the next state.
```python
@state(True)
def fire(shots):
    print("{} Shots fired!".format(shots))
    myFsm.nextState()
    pass
```

### Events

The FSM houses several events that trigger based on the current FSM state.

* onStateReached
* onDestinationReached

```python
from pyfsm.fsmLib import *
from pyfsm.fsmGlobals import *

def callOnStateReached():
    print("Reached a state")
    pass

def callOnDestReached():
    print("Reached the destination")
    pass

global myFsm 
myFsm = FSM(idle)

myFsm.onStateReached(callOnStateReached)
myFsm.onDestinationReached(callOnDestReached)
```

### FSM Creation

**To construct the FSM instance you need to pass as an argument the initial state of the FSM.**

To create the lifecycle of the FSM you can either:
- Create it manually by using the fsm.createTransition() method, as shown in the simpleExample script.
```python
from pyfsm.fsmLib import *
from pyfsm.fsmGlobals import *

global myFsm 
myFsm = FSM(idle)

myFsm.createTransition(idle, load, loading)
myFsm.createTransition(load, aim, aiming)
myFsm.createTransition(aim, fire)
myFsm.createTransition(fire, idle)
```

- Or parse a MermaidJS diagram:
```python
from pyfsm.fsmLib import *
from pyfsm.fsmGlobals import *

_stateDiagramTest = """
        ---
        title: Simple sample
        ---
        stateDiagram-v2
            idle --> load: "loading"
            load --> aim: "aiming"
            aim --> fire
            fire --> idle
        """

global myFsm 
myFsm = FSM(idle)

myFsm.createTransitionsFromDiagram(_stateDiagramTest)
```
> The full list of MermaidJS parsing format can be found at the Maslas Bros [MerParser](https://github.com/MaslasBros/pyStateGram) repository.

## Compatibility

This parser is compatible with any version equall or greater than [IronPython 3.4.1](https://ironpython.net/) and its Python equivalent which is Python 3.4.

*__Note__: IronPython3.4.1 support some Python 3.6 features which are listed in its website and [repository](https://github.com/IronLanguages/ironpython3).*

## Dependencies

* IronPython dependencies 
  
  * [IronPython 3.4.1 site](https://ironpython.net/)
  * [IronPython 3.4.1 repository](https://github.com/IronLanguages/ironpython3)
