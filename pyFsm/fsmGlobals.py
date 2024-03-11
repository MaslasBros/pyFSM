fsms = {}
"""Stores every fsm with a unique ID"""

stateCache = {}
"""Stores the registered state methods"""
transCache = {}
"""Stores the registered transitions methods"""

gStates = []
"""Contains the state dictionaries of each FSM accessed by the FSMs UID"""
gTransitions = []
"""Contains the transition dictionaries of each FSM accessed by the FSMs UID"""

def _addToTempStates(stateFunc, waitsForCallback):
    """
    Adds the passed state function to the internal states list.

    Args:
        stateFunc (:class:`func`): The function containing the state logic.
        waitsForCallback (:class:`bool`): Whether the FSM should wait for the callNextState callback to continue execution.

    Raises:
        (:class:`ValueError`): if the state function is already imported or registered as a state.
    """

    if stateCache.get(stateFunc.__name__):
        raise ValueError("Passed state " + stateFunc.__name__ + " already imported.")
    
    if transCache.get(stateFunc.__name__):
        raise ValueError("Passed transition " + stateFunc.__name__ + " is registered as a state.")
    
    stateCache[stateFunc.__name__] = (stateFunc, waitsForCallback)

def _addToTempTransitions(transFunc, waitsForCallback):
    """
    Adds the passed transition function to the internal transitions list.

    Args:
        transFunc (:class:`func`): The function containing the transition logic.
        waitsForCallback (:class:`bool`): Whether the FSM should wait for the callNextState callback to continue execution.

    Raises:
        (:class:`ValueError`): if the transition function is already imported or registered as a state.
    """

    if transCache.get(transFunc.__name__):
        raise ValueError("Passed transition " + transFunc.__name__ + " already imported.")
    
    if stateCache.get(transFunc.__name__):
        raise ValueError("Passed transition " + transFunc.__name__ + " is registered as a state.")
    
    transCache[transFunc.__name__] = (transFunc, waitsForCallback)

def state(waitsForCallback = False):
    """
    Decorator used to add the decorated method to the states list.

    Args:
        waitsForCallback(:class:`bool`, default = False): Whether the FSM should wait for the callNextState callback to continue execution.
    """

    if callable(waitsForCallback):
        _addToTempStates(waitsForCallback, False)
        return waitsForCallback

    def wrapper(func):
        _addToTempStates(func, waitsForCallback)
        return func

    return wrapper

def transition(waitsForCallback = False):
    """
    Decorator used to add the decorated method to the transition list.

    Args:
        waitsForCallback(:class:`bool`, default = False): Whether the FSM should wait for the callNextState callback to continue execution.
    """

    if callable(waitsForCallback):
        _addToTempTransitions(waitsForCallback, False)
        return waitsForCallback

    def wrapper(func):
        _addToTempTransitions(func, waitsForCallback)
        return func

    return wrapper