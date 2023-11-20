#FSM Relative
from .fsmGlobals import *
from .heuristics import *
from .eventHandler import *
#Merparser integration
from .mermaidHandler import *

#Python relative
from enum import Enum

#region FSM Local
class FSMStates(Enum):
    """
    All the available states the FSM can be in internally.
    """
    
    IDLING = -1, #When in any other state than the initial state
    IN_INITIAL_STATE = 0, # When in the initial state
    IN_RUNNING_STATE = 1, # When running a state
    IN_TRANSITION = 2, # When in a transition
    WAITING_FOR_CB = 3,
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

    def onStateReached(self, *func):
        """
        Adds the passed functions as an event callback of the state reached event.
        """
        self._eventHandler.subscribeToEvent(self.EVENT_STATE_REACHED_NAME, *func)
        pass

    def onDestinationReached(self, *func):
        """
        Adds the passed function as an event callback of the destination reached event.
        """
        self._eventHandler.subscribeToEvent(self.EVENT_DESTINATION_REACHED_NAME, *func)
        pass

    def __init__(self, initialState):
        """
        Constructs a FSM instance with empty states and transitions.\n
        The initial state must either be the state string name or the state function.
        """

        self._registerFsm()
        self._eventHandler = EventDispatcher(self.EVENT_STATE_REACHED_NAME, self.EVENT_DESTINATION_REACHED_NAME)
        self._fsmInternalState = FSMStates.IN_INITIAL_STATE

        self.initialState = initialState.__name__ if not isinstance(initialState, str) else initialState
        self.currentGraphState = self.initialState
        self._statePairs = []
        self._routes = {}
        self._cachedDestState = None

        #Merparser integration
        self.mermaidHandler = MermaidHandler(self)
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

        cStateName = currentState[0].__name__ if isinstance(currentState, tuple) else currentState.__name__
        nStateName = nextState[0].__name__ if isinstance(nextState, tuple) else nextState.__name__

        #Checks for None transition
        if transition is not None:
            trName = transition[0].__name__ if isinstance(transition, tuple) else transition.__name__
            gTransitions[self.uid][trName] = transCache[trName]

        #Register the retrieved states and transitions to this FSM instance
        gStates[self.uid][cStateName] = stateCache[cStateName]
        gStates[self.uid][nStateName] = stateCache[nStateName]
        
        #Create the state-transition pairs
        self._statePairs.append((gStates[self.uid][cStateName], gStates[self.uid][nStateName], transition))

        #Create the dynamic methods for the two new states
        if getattr(self,cStateName, self._dynamicMethodWrapper(gStates[self.uid][cStateName])) is not None:
            setattr(self, cStateName, self._dynamicMethodWrapper(gStates[self.uid][cStateName]))

        if getattr(self, nStateName, self._dynamicMethodWrapper(gStates[self.uid][nStateName])) is not None:
            setattr(self, nStateName, self._dynamicMethodWrapper(gStates[self.uid][nStateName]))

        self._buildRoutesGraph()

        return self

    def createTransitionsFromDiagram(self, mermaidDiagram:str):
        """
        Dynamically creates the states and transitions from the provided mermaid diagram.\n
        Diagram Sample:\n
        
        ```text
        stateDiagram-v2\n
            idle --> load: "loading" - state transition with a transition method named "loading" \n
            idle --> release - state transitions with no transition method \n
            load --> aim: "aiming" - state transition with a transition method named "aiming" \n
        ```
        """
        self.mermaidHandler.createTransitionsFromDiagram(mermaidDiagram)
        pass

    def _dynamicMethodWrapper(self, stateFuncTupple):
        """
        This method is a state function wrapper to add the self return at each state method.\n
        This enables method piping support for the FSM.
        """

        def wrapper(*args, **kwargs) -> self:
            #Do not continue on the next state if the currentState is waiting for a callback
            if self.getInternalFsmState() is FSMStates.WAITING_FOR_CB:
                return

            self._traverseToState(stateFuncTupple[0].__name__, *args, *kwargs)
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
        
        self._cachedDestState = (destStateName, *args, *kwargs)
        route = self._routes[self.currentGraphState][destStateName]
        #print("Route to {} is {}".format(destStateName, str(route)))

        #iterates in the state-transition tuples inside the route queue
        for stateTupple, trans in route:
            if trans is not None:
                self._setInternalFsmState(FSMStates.IN_TRANSITION)
                #gTransitions[self.uid][trans][0]()
                self._eventHandler.raiseEvent(self.EVENT_STATE_REACHED_NAME)

    
            self._setInternalFsmState(FSMStates.IN_RUNNING_STATE)

            state, wfc = gStates[self.uid][stateTupple]

            if state.__name__ is destStateName:
                self._eventHandler.raiseEvent(self.EVENT_DESTINATION_REACHED_NAME)
                state(*args, **kwargs)
            else:
                self._eventHandler.raiseEvent(self.EVENT_STATE_REACHED_NAME)
                state()

            self.currentGraphState = state.__name__
            self._determineInternalFsmState()

            #Do not continue on the next state if the currentState is waiting for a callback
            if wfc:
                self._setInternalFsmState(FSMStates.WAITING_FOR_CB)
                print("Waiting for state cb")
                break
        pass
    
    def continueTraversal(self):
        '''
        Pass this method as a callback function to an external source to continue with
        the FSMs normal traversing flow. 
        '''
        
        self._setInternalFsmState(FSMStates.IDLING)
        self._traverseToState(self._cachedDestState[0], self._cachedDestState[1])
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

    def forceChangeState(self, stateName:str, *args, **kwargs):
        """
        Forcefully call and set the current state of the FSM to the passed state name.
        """
        self._setInternalFsmState(FSMStates.IDLING)
        self.currentGraphState = stateName
        gStates[self.uid][self.currentGraphState][0](*args, **kwargs)

    def forceResetFSM(self):
        """
        Forcefully reset the FSM without traversing from the current state back to the initial state.
        """
        gStates[self.uid][self.initialState]()
        self.currentGraphState = self.initialState
        pass
#endregion