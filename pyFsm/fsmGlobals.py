fsms = {} # Stores every fsm with a unique ID

stateCache = {} # Stores the registered state methods
transCache = {} # stores the registered transitions methods

gStates = [] # Contains the state dictionaries of each FSM accessed by the FSMs UID
gTransitions = [] # Contains the transition dictionaries of each FSM accessed by the FSMs UID

def _addToTempStates(stateFunc):
    """
    Adds the passed state function to the internal states list.\n
    Throws an error if the state function is already imported or registered as a state.
    """

    if stateCache.get(stateFunc.__name__):
        raise ValueError("Passed state " + stateFunc.__name__ + " already imported.")
    
    if transCache.get(stateFunc.__name__):
        raise ValueError("Passed transition " + stateFunc.__name__ + " is registered as a state.")
    
    stateCache[stateFunc.__name__] = stateFunc

def _addToTempTransitions(transFunc):
    """
    Adds the passed transition function to the internal transitions list.\n
    Throws an error if the transition function is already imported or registered as a state.
    """

    if transCache.get(transFunc.__name__):
        raise ValueError("Passed transition " + transFunc.__name__ + " already imported.")
    
    if stateCache.get(transFunc.__name__):
        raise ValueError("Passed transition " + transFunc.__name__ + " is registered as a state.")
    
    transCache[transFunc.__name__] = transFunc

def state(stateFunc):
    """
    Decorator used to add the decorated method to the states list
    """

    _addToTempStates(stateFunc)
    return stateFunc

def transition(transFunc):
    """
    Decorator used to add the decorated method to the transition list.
    All transition methods must return a boolean value, which determines 
    """

    """ if isinstance(transFunc(), bool) is not True:
        raise ValueError("Transition \'" + transFunc.__name__ + "\' does not return a boolean to verify the transition.") """

    _addToTempTransitions(transFunc)
    return transFunc