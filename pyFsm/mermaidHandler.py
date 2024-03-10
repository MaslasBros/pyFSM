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

        Args:
            ownFsm (:class:`FSM`): The FSM instance caching this MermaidHandler instance.

        Attributes:
            ~ pyfsm.mermaidHandler.MermaidHandler.ownFsm (:class:`FSM`): The FSM instance caching this MermaidHandler instance.
            ~ pyfsm.mermaidHandler.MermaidHandler.package (:class:`DiagramPackage`): The FSM instance caching this MermaidHandler instance.
        """
        self.ownFsm = ownFsm #type: FSM
        self.package = None #type: DiagramPackage
        pass

    def createTransitionsFromDiagram(self, mermaidDiagram:str):
        """
        Dynamically creates the states and transitions from the provided mermaid diagram.
        
        Diagram Sample:
        
        ```text
            stateDiagram-v2\n
                idle --> load: "loading" - state transition with a transition method named "loading" \n
                idle --> release - state transitions with no transition method \n
                load --> aim: "aiming" - state transition with a transition method named "aiming" \n
        ```

        Args:
            mermaidDiagram (:class:`str`): The mermaid diagram to parse.
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
        """
        Returns the parsed mermaid diagram package.

        For better accessing use the below (:class:`funcs`):

            `MermaidHandler.accessMermaidDiagramStates`
            
            `MermaidHandler.accessMermaidDiagramTransitions`

        
        Returns:
            A `DiagramPackage` instance containing the states and transitions.
        """
        return self.package

    def accessMermaidDiagramStates(self) -> dict:
        """Returns the parsed mermaid diagram states dictionary."""
        return self.package.states
    
    def accessMermaidDiagramTransitions(self) -> dict:
        """Returns the parsed mermaid diagram transitions dictionary."""
        return self.package.transitions