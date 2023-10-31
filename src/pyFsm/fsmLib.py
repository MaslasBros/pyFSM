#region Global
_fsms = {} # Stores every fsm with a unique ID

_stateCache = {} # Stores the registered state methods
_transCache = {} # stores the registered transitions methods

_gStates = [] # Contains the state dictionaries of each FSM accessed by the FSMs UID
_gTransitions = [] # Contains the transition dictionaries of each FSM accessed by the FSMs UID

def _addToTempStates(stateFunc):
    """
    Adds the passed state function to the internal states list.\n
    Throws an error if the state function is already imported or registered as a state.
    """

    if _stateCache.get(stateFunc.__name__):
        raise ValueError("Passed state " + stateFunc.__name__ + " already imported.")
    
    if _transCache.get(stateFunc.__name__):
        raise ValueError("Passed transition " + stateFunc.__name__ + " is registered as a state.")
    
    _stateCache[stateFunc.__name__] = stateFunc

def _addToTempTransitions(transFunc):
    """
    Adds the passed transition function to the internal transitions list.\n
    Throws an error if the transition function is already imported or registered as a state.
    """

    if _transCache.get(transFunc.__name__):
        raise ValueError("Passed transition " + transFunc.__name__ + " already imported.")
    
    if _stateCache.get(transFunc.__name__):
        raise ValueError("Passed transition " + transFunc.__name__ + " is registered as a state.")
    
    _transCache[transFunc.__name__] = transFunc

def state(stateFunc):
    """
    Decorator used to add the decorated method to the states list
    """

    _addToTempStates(stateFunc)
    return stateFunc

def transition(transFunc):
    """
    Decorator used to add the decorated method to the transition list
    """

    _addToTempTransitions(transFunc)
    return transFunc
#endregion

#region FSM Local
class FSM:
    #@TODO: Integrate merparser
    def __init__(self):
        """
        Constructs a FSM instance with empty states and transitions.\n
        """

        self._registerFsm()

        self.statePairs = []
        pass

    def _registerFsm(self):
        """
        Registers the FSM instance to the global FSM cache of the script.\n
        The UID of the FSM is also assigned here.\n
        Raises an error in case the FSM is already registered.
        """
        
        self.uid = len(_fsms)

        if _fsms.get(self.uid):
            raise KeyError("FSM with UID: " + self.uid + " already registered.")
        
        _fsms[self.uid] = self
        _gStates.append({})
        _gTransitions.append({})

    def _retrieveStateFromCache(self, stateName:str):
        """
        Returns the cached state method from the global state cache, then deletes it.\n
        """
        
        _cache = _stateCache[stateName]
        #_stateCache[_cache] = None

        return _cache
    
    def _retrieveTransitionFromCache(self, transitionName:str):
        """
        Returns the cached transition method from the global transition cache, then deletes it.\n
        """

        _cache = _transCache[transitionName]
        #_transCache[_cache] = None

        return _cache

    def createTransition(self, currentState, nextState, transition = None):
        """
        Creates a new state transition which the current state transits to the next state through the passed transition.\n
        If the passed transition is None, then the state transition is instant.
        """

        #Checks for None transition
        if transition is not None:
            _gTransitions[self.uid][transition.__name__] = self._retrieveTransitionFromCache(transition.__name__)

        #Register the retrieved states and transitions to this FSM instance
        _gStates[self.uid][currentState.__name__] = self._retrieveStateFromCache(currentState.__name__)
        _gStates[self.uid][nextState.__name__] = self._retrieveStateFromCache(nextState.__name__)
        
        #Create the state-transition pairs
        self.statePairs.append((currentState, nextState, transition))

        #Create the dynamic methods for the two new states
        if getattr(self, currentState.__name__, self._dynamicMethodWrapper(_gStates[self.uid][currentState.__name__])) is not None:
            setattr(self, currentState.__name__, self._dynamicMethodWrapper(_gStates[self.uid][currentState.__name__]))

        if getattr(self, nextState.__name__, self._dynamicMethodWrapper(_gStates[self.uid][nextState.__name__])) is not None:
            setattr(self, nextState.__name__, self._dynamicMethodWrapper(_gStates[self.uid][nextState.__name__]))

        return self

    def createTransitionFromDiagram(self, mermaidDiagram:str):
        #@TODO:
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

    #region UTILS
    def printStates(self):
        for i in _gStates[self.uid]:
            print(i)
        pass

    def printTransitions(self):
        for i in _gTransitions[self.uid]:
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