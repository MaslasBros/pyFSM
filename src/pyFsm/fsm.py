states = []
transitions = []

def _addToStates(stateFunc):
    """
    Adds the passed state function to the internal states list.\n
    Throws an error if the state function is already imported or registered as a state.
    """

    if stateFunc in states:
        raise ValueError("Passed state " + stateFunc.__name__ + " already imported.")
    
    if stateFunc in transitions:
        raise ValueError("Passed transition " + stateFunc.__name__ + " is registered as a state.")
    
    states.append(stateFunc)

def _addToTransitions(transFunc):
    """
    Adds the passed transition function to the internal transitions list.\n
    Throws an error if the transition function is already imported or registered as a state.
    """

    if transFunc in transitions:
        raise ValueError("Passed transition " + transFunc.__name__ + " already imported.")
    
    if transFunc in states:
        raise ValueError("Passed transition " + transFunc.__name__ + " is registered as a state.")
    
    transitions.append(transFunc)

def state(stateFunc):
    """
    Decorator used to add the registered method to the states list
    """

    _addToStates(stateFunc)
    return stateFunc

def transition(transFunc):
    """
    Decorator used to add the registered method to the transition list
    """

    _addToTransitions(transFunc)
    return transFunc

def createTransition(currentState, nextState):
    #@TODO:
    pass

def createTransition(currentState, transition, nextState):
    #@TODO:
    pass

#region UTILS
def printStates():
    for i in states:
        print(i.__name__)
    pass

def printTransitions():
    for i in transitions:
        print(i.__name__)
    pass
#endregion