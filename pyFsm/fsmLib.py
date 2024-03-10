#FSM Relative
from . import fsmGlobals as globals
from . import heuristics as sort
from . import eventHandler as events
#Merparser integration
from . import mermaidHandler as merParser

#Python relative
import inspect
from enum import Enum
from queue import Queue

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
        
        Args:
           initialState (:class:`str` or `func`): The initial state must either be the state string name or the state function.

        Attributes:
            ~ pyFsm.fsmLib.FSM.uid: The FSM assigned to this fsm
            ~ pyFsm.fsmLib.FSM._eventHandler: The FSM event handler
            ~ pyFsm.fsmLib.FSM._fsmInternalState: The FSM `FSMStates` state for FSM management
            ~ pyFsm.fsmLib.FSM.initialState: The FSM initial state given from the constructor
            ~ pyFsm.fsmLib.FSM.currentGraphState: The same as `initialState`
            ~ pyFsm.fsmLib.FSM._statePairs: The state-transition pairs of this FSM
            ~ pyFsm.fsmLib.FSM._routes: The state to state shortest routes.
            ~ pyFsm.fsmLib.FSM._destQueue: The destination state name when transitions from state to state.
            ~ pyFsm.fsmLib.FSM._destQueue: A queue used in conjuction with the nextState method to cache the states that must be passed until the destination state is reached.
            ~ pyFsm.fsmLib.FSM.mermaidHandler: The `MermaidHandler` of this FSM used for Mermaid JS parsing.
        """

        self.uid = -1
        """The FSM id"""
        self._registerFsm()
        self._eventHandler = events.EventDispatcher(self.EVENT_STATE_REACHED_NAME, self.EVENT_DESTINATION_REACHED_NAME)
        """The FSM event handler"""
        self._fsmInternalState = FSMStates.IN_INITIAL_STATE
        """The FSM `FSMStates` state for FSM management"""

        self.initialState = initialState.__name__ if not isinstance(initialState, str) else initialState
        """The FSM initial state given from the constructor"""
        self.currentGraphState = self.initialState
        """The current state the FSM is in until it reaches the destination state"""
        self._statePairs = []
        """The state-transition pairs of this FSM"""
        self._routes = {}
        """The state to state shortest routes."""
        self._cachedDestState = None
        """The destination state name when transitions from state to state."""
        self._destQueue = Queue()
        """A queue used in conjuction with the nextState method to cache the states that must be passed until the destination state is reached."""

        #Merparser integration
        self.mermaidHandler = merParser.MermaidHandler(self)
        """The `MermaidHandler` of this FSM"""
        pass

    def _registerFsm(self):
        """
        Registers the FSM instance to the global FSM cache of the script.\n
        The UID of the FSM is also assigned here.\n

        Raises:
            (:class:`KeyError`): In case the FSM is already registered.
        """
        
        self.uid = len(globals.fsms)

        if globals.fsms.get(self.uid):
            raise KeyError("FSM with UID: " + self.uid + " already registered.")
        
        globals.fsms[self.uid] = self
        globals.gStates.append({})
        globals.gTransitions.append({})
        pass

    def createTransition(self, currentState, nextState, transition = None):
        """
        Creates a new state transition which the current state transits to the next state through the passed transition.\n
        If the passed transition is None, then the state transition is instant.

        Args:
            currentState (:class:`tuple` or `func`): The source state function
            nextState (:class:`tuple` or `func`): The target state function
            transition (:class:`tuple` or `func`, default = None): The transition function, if any
        """

        cStateName = currentState[0].__name__ if isinstance(currentState, tuple) else currentState.__name__
        nStateName = nextState[0].__name__ if isinstance(nextState, tuple) else nextState.__name__

        #Checks for None transition
        if transition is not None:
            trName = transition[0].__name__ if isinstance(transition, tuple) else transition.__name__
            globals.gTransitions[self.uid][trName] = globals.transCache[trName]

        #Register the retrieved states and transitions to this FSM instance
        globals.gStates[self.uid][cStateName] = globals.stateCache[cStateName]
        globals.gStates[self.uid][nStateName] = globals.stateCache[nStateName]
        
        #Create the state-transition pairs
        self._statePairs.append((globals.gStates[self.uid][cStateName], globals.gStates[self.uid][nStateName], transition))

        #Create the dynamic methods for the two new states
        if getattr(self,cStateName, self._dynamicMethodWrapper(globals.gStates[self.uid][cStateName])) is not None:
            setattr(self, cStateName, self._dynamicMethodWrapper(globals.gStates[self.uid][cStateName]))

        if getattr(self, nStateName, self._dynamicMethodWrapper(globals.gStates[self.uid][nStateName])) is not None:
            setattr(self, nStateName, self._dynamicMethodWrapper(globals.gStates[self.uid][nStateName]))

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

        Args:
            mermaidDiagram (:class:`str`): The mermaid diagram to parse
        """
        self.mermaidHandler.createTransitionsFromDiagram(mermaidDiagram)
        pass

    def _dynamicMethodWrapper(self, stateFuncTuple):
        """
        This method is a state function wrapper to add the `self return` at each state method.\n
        This enables method piping support for the FSM.

        Args:
            stateFuncTuple (:class:`tuple`): Tuple containg the state current-next state pairs.
        """

        def wrapper(*args, **kwargs):
            #Do not continue on the next state if the currentState is waiting for a callback
            if self.getInternalFsmState() is FSMStates.WAITING_FOR_CB:
                return

            #Adds the called state to the transitions queue, this enables piping support.
            return self._addToDestQueue(stateFuncTuple[0].__name__, *args, **kwargs)
        return wrapper

    def _addToDestQueue(self, methodName:str, *args):
        """
        Adds the passed method string and its arguments to the _destQueue of the FSM.
        
        Args:
            methodName (:class:`str`): The method name to add to the destination queue
            args: The arguments to pass to the method.
        """
        self._destQueue.put((methodName, *args))
        return self

    def _buildRoutesGraph(self):
        """
        Creates the routes graph containing all possible state transitions along with their shortest routes and transitions.
        """
        
        graph = sort.buildStateGraph(self._statePairs)
        self._routes = sort.findShortestRoutes(graph)
        pass

    def run(self):
        """
        Call this method to start the FSM normal execution of states and transitioning.
        """
        while not self._destQueue.qsize() == 0:
            if self.getInternalFsmState() is FSMStates.WAITING_FOR_CB:
                break

            cState, *args = self._destQueue.get()
            self._traverseToState(cState, *args)

        pass

    def _traverseToState(self, destStateName:str, *args, **kwargs):
        """
        Traverses to the passed destination state from the current state the FSM is at.

        * Args and kwargs are passed only in the requested destination state and not in the states in-between.

        Args:
            destStateName (:class:`str`): The state to traverse to.
            args: The arguments to pass to the destination method.
            kwargs: The arguments to pass to the destination method.
        """
        
        self._cachedDestState = (destStateName, *args, *kwargs)
        route = self._routes[self.currentGraphState][destStateName]
        #print("Route to {} is {}".format(destStateName, str(route)))

        #iterates in the state-transition tuples inside the route queue
        for stateTupple, transTuple in route:
            #Transition handling
            if transTuple is not None:
                self._setInternalFsmState(FSMStates.IN_TRANSITION)
                trans, wfc = globals.gTransitions[self.uid][transTuple]
                trans()
                self._eventHandler.raiseEvent(self.EVENT_STATE_REACHED_NAME)
    
            self._setInternalFsmState(FSMStates.IN_RUNNING_STATE)

            #State handling
            state, wfc = globals.gStates[self.uid][stateTupple]
            self.currentGraphState = state.__name__

            if state.__name__ is destStateName:
                self._eventHandler.raiseEvent(self.EVENT_DESTINATION_REACHED_NAME)
                self._cachedDestState = None
                
                if inspect.signature(state).parameters:
                    state(*args, **kwargs)
                else:
                    state()
                    
            else:
                self._eventHandler.raiseEvent(self.EVENT_STATE_REACHED_NAME)
                state()

            self._determineInternalFsmState()

            #Do not continue on the next state if the currentState is waiting for a callback
            if wfc:
                self._setInternalFsmState(FSMStates.WAITING_FOR_CB)
                break
        pass
    
    def nextState(self):
        '''
        Pass this method as a callback function to an external source to continue with
        the FSMs normal traversing flow. 
        '''

        if self._cachedDestState == None:
            self.run()
        else:
            self._traverseToState(self._cachedDestState[0], self._cachedDestState[1] if self._cachedDestState.__len__() > 1 else None)
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

        Args:
            newState (:enum:`FSMStates`): The new state
        """
        self._fsmInternalState = newState 
        pass

    def forceChangeState(self, stateName:str, *args, **kwargs):
        """
        Forcefully call and set the current state of the FSM to the passed state name.

        Args:
            stateName (:class:`str`): The state to change into the FSM current state into.
            args: The arguments to pass to the state method.
            kwargs: The arguments to pass to the state method.
        """
        self._setInternalFsmState(FSMStates.IDLING)
        self.currentGraphState = stateName
        globals.gStates[self.uid][self.currentGraphState][0](*args, **kwargs)

    def forceResetFSM(self):
        """
        Forcefully reset the FSM without traversing from the current state back to the initial state of the FSM.
        """
        globals.gStates[self.uid][self.initialState]()
        self.currentGraphState = self.initialState
        pass
#endregion