class FSM:
    #@TODO: Integrate merparser
    def __init__(self):
        """
        Constructs a FSM instance with empty states and transitions.\n
        """
        
        self.states = []
        self.transitions = []
        self.statePairs = []

        pass

    def _addToStates(self, stateFunc):
        """
        Adds the passed state function to the internal states list.\n
        Throws an error if the state function is already imported or registered as a state.
        """

        if stateFunc in self.states:
            raise ValueError("Passed state " + stateFunc.__name__ + " already imported.")
        
        if stateFunc in self.transitions:
            raise ValueError("Passed transition " + stateFunc.__name__ + " is registered as a state.")
        
        self.states.append(stateFunc)
        setattr(self, stateFunc.__name__, self._dynamicMethodWrapper(stateFunc))

    def _dynamicMethodWrapper(self, stateFunc):
        """
        This method is a state function wrapper to add the self return at each state method.\n
        This enables method piping support for the FSM.
        """

        def wrapper(*args, **kwargs) -> self:
            stateFunc(*args, **kwargs)
            return self
        return wrapper

    def _addToTransitions(self, transFunc):
        """
        Adds the passed transition function to the internal transitions list.\n
        Throws an error if the transition function is already imported or registered as a state.
        """

        if transFunc in self.transitions:
            raise ValueError("Passed transition " + transFunc.__name__ + " already imported.")
        
        if transFunc in self.states:
            raise ValueError("Passed transition " + transFunc.__name__ + " is registered as a state.")
        
        self.transitions.append(transFunc)

    def state(self, stateFunc):
        """
        Decorator used to add the registered method to the states list
        """

        self._addToStates(stateFunc)
        return stateFunc

    def transition(self, transFunc):
        """
        Decorator used to add the registered method to the transition list
        """

        self._addToTransitions(transFunc)
        return transFunc

    def createTransition(self, currentState, nextState ,transition = None):
        """
        Creates a new state transition which the current state transits to the next state through the passed transition.\n
        If the passed transition is None, then the state transition is instant.
        """

        self.statePairs.append((currentState,nextState, transition))
        pass

    #region UTILS
    def printStates(self):
        for i in self.states:
            print(i.__name__)
        pass

    def printTransitions(self):
        for i in self.transitions:
            print(i.__name__)
        pass

    def printStatePairs(self):
        for i in self.statePairs:
            print(i[0].__name__ + " transits to " + i[1].__name__)
            if i[2] is not None:
                print("-> with transition " + i[2].__name__)
        pass
    #endregion