from .fsmGlobals import *
from .fsmLib import *

#Merparser import
from .pyStateGram.pystategram import *

class MermaidHandler:
    """
    This class is responsible for the Mermaid JS parsing feature of the python FSM.\n
    Stores the parsed DiagramPackage, states and transitions from the passed Mermaid graph.  
    """
    def __init__(self, ownFsm):
        """
        Creates a MermaidHandler instance and assigns the passed FSM as its FSM handler.
        """
        self.ownFsm = ownFsm #type: FSM
        self.package = None #type: DiagramPackage
        pass

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
    
        self.package = parseStateDiagram(mermaidDiagram)

        for transName, transObj in self.accessMermaidDiagramTransitions().items():
            if transName != str(transObj.source + '_' + transObj.target): # Has transition method
                self.ownFsm.createTransition(stateCache[transObj.source], stateCache[transObj.target], transCache[transName])
            else: # Does not have transition method
                self.ownFsm.createTransition(stateCache[transObj.source], stateCache[transObj.target])
            pass
        pass

    def accessMermaidDiagram(self) -> DiagramPackage:
        """Returns the parsed mermaid diagram package."""
        return self.package

    def accessMermaidDiagramStates(self) -> dict:
        """Returns the parsed mermaid diagram states dictionary."""
        return self.package.states
    
    def accessMermaidDiagramTransitions(self) -> dict:
        """Returns the parsed mermaid diagram transitions dictionary."""
        return self.package.transitions