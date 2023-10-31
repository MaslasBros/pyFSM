#region Global
_states = {}
_transitions = {}

def _addToStates(stateFunc):
    """
    Adds the passed state function to the internal states list.\n
    Throws an error if the state function is already imported or registered as a state.
    """

    if _states.get(stateFunc.__name__):
        raise ValueError("Passed state " + stateFunc.__name__ + " already imported.")
    
    if _transitions.get(stateFunc.__name__):
        raise ValueError("Passed transition " + stateFunc.__name__ + " is registered as a state.")
    
    _states[stateFunc.__name__] = stateFunc

def _addToTransitions(transFunc):
    """
    Adds the passed transition function to the internal transitions list.\n
    Throws an error if the transition function is already imported or registered as a state.
    """

    if _transitions.get(transFunc.__name__):
        raise ValueError("Passed transition " + transFunc.__name__ + " already imported.")
    
    if _states.get(transFunc.__name__):
        raise ValueError("Passed transition " + transFunc.__name__ + " is registered as a state.")
    
    _transitions[transFunc.__name__] = transFunc

def state(stateFunc):
    """
    Decorator used to add the decorated method to the states list
    """

    _addToStates(stateFunc)
    return stateFunc

def transition(transFunc):
    """
    Decorator used to add the decorated method to the transition list
    """

    _addToTransitions(transFunc)
    return transFunc
#endregion

#region FSM Local
class FSM:
    #@TODO: Integrate merparser
    def __init__(self):
        """
        Constructs a FSM instance with empty states and transitions.\n
        """

        self.statePairs = []
        self._dynamicMethodCreator()
        pass

    def _dynamicMethodCreator(self):
        """
        Adds a dynamic method for each state function from the _states dictionary
        in this FSM instance. 
        """

        for stateFunc in _states:
            setattr(self, stateFunc, self._dynamicMethodWrapper(_states[stateFunc]))
        pass

    def _dynamicMethodWrapper(self, stateFunc):
        """
        This method is a state function wrapper to add the self return at each state method.\n
        This enables method piping support for the FSM.
        """

        def wrapper(*args, **kwargs) -> self:
            stateFunc(*args, **kwargs)
            return self
        return wrapper

    def createTransition(self, currentState, nextState, transition = None):
        """
        Creates a new state transition which the current state transits to the next state through the passed transition.\n
        If the passed transition is None, then the state transition is instant.
        """

        self.statePairs.append((currentState,nextState, transition))
        return self

    #region UTILS
    def printStates(self):
        for i in _states:
            print(i)
        pass

    def printTransitions(self):
        for i in _transitions:
            print(i)
        pass

    def printStatePairs(self):
        for i in self.statePairs:
            print(i[0].__name__ + " transits to " + i[1].__name__)
            if i[2] is not None:
                print("-> with transition " + i[2].__name__)
        pass
    #endregion
#endregion