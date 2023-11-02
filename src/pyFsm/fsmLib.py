#FSM Relative
from .fsmGlobals import *
from .heuristics import *
from .eventHandler import *

#Python relative
from enum import Enum
from threading import Thread

#region FSM Local
class FSMStates(Enum):
    """
    All the available states the FSM can be in internally.
    """
    
    IDLING = -1, #When in any other state than the initial state
    IN_INITIAL_STATE = 0, # When in the initial state
    IN_RUNNING_STATE = 1, # When running a state
    IN_TRANSITION = 2, # When in a transition
    pass

class FSM:
    EVENT_STATE_REACHED_NAME = 'StateReached'
    EVENT_DESTINATION_REACHED_NAME = 'DestinationReached'

    def getCurrentFsmState(self):
        """
        Returns the current state the FSM is at.
        """
        return self.currentGraphState
    
    def getInternalFsmState(self):
        """
        Returns the internal state of the FSM.
        """
        return self._fsmInternalState

    def onStateReached(self, func):
        """
        Adds the passed function as an event callback of the state reached event.
        """
        self._eventHandler.subscribeToEvent(self.EVENT_STATE_REACHED_NAME, func)
        pass

    def onDestinationReached(self, func):
        """
        Adds the passed function as an event callback of the destination reached event.
        """
        self._eventHandler.subscribeToEvent(self.EVENT_DESTINATION_REACHED_NAME, func)
        pass

    def __init__(self, initialState):
        """
        Constructs a FSM instance with empty states and transitions.\n
        """

        self._registerFsm()
        self._eventHandler = EventDispatcher(self.EVENT_STATE_REACHED_NAME, self.EVENT_DESTINATION_REACHED_NAME)
        self._fsmInternalState = FSMStates.IN_INITIAL_STATE

        self.initialState = initialState.__name__
        self.currentGraphState = self.initialState
        self._statePairs = []
        self._routes = {}
        pass

    def _registerFsm(self):
        """
        Registers the FSM instance to the global FSM cache of the script.\n
        The UID of the FSM is also assigned here.\n
        Raises an error in case the FSM is already registered.
        """
        
        self.uid = len(fsms)

        if fsms.get(self.uid):
            raise KeyError("FSM with UID: " + self.uid + " already registered.")
        
        fsms[self.uid] = self
        gStates.append({})
        gTransitions.append({})
        pass

    def createTransition(self, currentState, nextState, transition = None):
        """
        Creates a new state transition which the current state transits to the next state through the passed transition.\n
        If the passed transition is None, then the state transition is instant.
        """

        #Checks for None transition
        if transition is not None:
            gTransitions[self.uid][transition.__name__] = transCache[transition.__name__]

        #Register the retrieved states and transitions to this FSM instance
        gStates[self.uid][currentState.__name__] = stateCache[currentState.__name__]
        gStates[self.uid][nextState.__name__] = stateCache[nextState.__name__]
        
        #Create the state-transition pairs
        self._statePairs.append((currentState, nextState, transition))

        #Create the dynamic methods for the two new states
        if getattr(self, currentState.__name__, self._dynamicMethodWrapper(gStates[self.uid][currentState.__name__])) is not None:
            setattr(self, currentState.__name__, self._dynamicMethodWrapper(gStates[self.uid][currentState.__name__]))

        if getattr(self, nextState.__name__, self._dynamicMethodWrapper(gStates[self.uid][nextState.__name__])) is not None:
            setattr(self, nextState.__name__, self._dynamicMethodWrapper(gStates[self.uid][nextState.__name__]))

        self._buildRoutesGraph()

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
            if self.currentGraphState is not stateFunc.__name__:
                self._traverseToState(stateFunc.__name__, *args, *kwargs)
            else:
                self._setInternalFsmState(FSMStates.IN_RUNNING_STATE)
                self._runFunctionInThread(stateFunc, *args, **kwargs)
                self._determineInternalFsmState()
            return self
        return wrapper

    def _buildRoutesGraph(self):
        """
        Creates the routes graph containing all possible state transitions along with their shortest routes and transitions.
        """
        
        graph = buildStateGraph(self._statePairs)
        self._routes = findShortestRoutes(graph)
        pass

    def _traverseToState(self, destStateName:str, *args, **kwargs):
        """
        Traverses to the passed destination state from the current state the FSM is at.\n
        Args and kwargs are passed only in the requested destination state and not in the states in-between.\n
        """
        
        route = self._routes[self.currentGraphState][destStateName]
        #print("Route to {} is {}".format(destStateName, str(route)))

        #iterates in the state-transition tuples inside the route list
        for state, trans in route: 
            if trans is not None:
                self._setInternalFsmState(FSMStates.IN_TRANSITION)
                self._runFunctionInThread(gTransitions[self.uid][trans])
                self._eventHandler.raiseEvent(self.EVENT_STATE_REACHED_NAME)
                
            self._setInternalFsmState(FSMStates.IN_RUNNING_STATE)
            if state is destStateName:
                self._runFunctionInThread(gStates[self.uid][state], *args, **kwargs)
                self._eventHandler.raiseEvent(self.EVENT_DESTINATION_REACHED_NAME)
            else:
                self._runFunctionInThread(gStates[self.uid][state])
                self._eventHandler.raiseEvent(self.EVENT_STATE_REACHED_NAME)

            self.currentGraphState = state
            self._determineInternalFsmState()
        pass
    
    def _runFunctionInThread(self, function, *args, **kwargs):
        """
        Runs the passed function in a new thread and waits for its completion.\n
        Args and kwaargs can be None.
        """
        
        if len(args) != 0:
            thread = Thread(target = function,  args = args, kwargs = kwargs)
        else:
            thread = Thread(target = function)

        thread.start()
        thread.join()
        pass

    def _determineInternalFsmState(self):
        """
        Sets the internal FSM state based on its self.currentState value.
        """
        if self.currentGraphState is not self.initialState:
            self._fsmInternalState = FSMStates.IDLING
        else:
            self._fsmInternalState = FSMStates.IN_INITIAL_STATE    
        pass

    def _setInternalFsmState(self, newState:FSMStates):
        """
        Sets the internal FSM state to the passed value
        """
        self._fsmInternalState = newState 
        pass

    def forceResetFSM(self):
        """
        Forcefully reset the FSM without traversing from the current state back to the initial state.
        """
        gStates[self.uid][self.initialState]()
        self.currentGraphState = self.initialState
        pass
#endregion