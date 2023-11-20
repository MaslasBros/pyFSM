from collections import deque

def buildStateGraph(statePairs:[]) -> dict:
    """
    Creates a state graph from different imported state pairs
    containing state -> state and their transitions functions.\n
    Returns a dictionary containing all the transitions from a state to an other state
    with stateNames as keys.
    """
    
    stateGraph = {}
    for state, nextState, trans in statePairs:
        stateName = state.__name__ if not isinstance(state, tuple) else state[0].__name__
        nextStateName = nextState.__name__ if not isinstance(nextState, tuple) else nextState[0].__name__
        #transName = trans.__name__ if trans is not None else None
        transName = ''
        if trans is not None:
            transName = trans[0].__name__ if isinstance(trans, tuple) else trans.__name__
        else:
            transName = None

        if stateName not in stateGraph:
            stateGraph[stateName] = []

        stateGraph[stateName].append((nextStateName, transName))

        if nextStateName not in stateGraph:
            stateGraph[nextStateName] = []

    return stateGraph

def findShortestRoutes(stateGraph:{}) -> dict:
    """
    Creates a dictionary which contains the shortest route from one state to all of the other states.\n
    Accessible by the state names.
    """
    
    shortestRoutes = {}

    for startState in stateGraph:
        shortestRoutes[startState] = {}
        visited = set()
        queue = deque([(startState, [])])

        while queue:
            currentState, path = queue.popleft()
            if currentState not in visited:
                visited.add(currentState)
                shortestRoutes[startState][currentState] = path

                for nextState, trans in stateGraph[currentState]:
                    if nextState not in visited:
                        queue.append((nextState, path + [(nextState, trans)]))

    return shortestRoutes