class EventDispatcher:
    """
    Simple implementation of an event dispatcher.
    """
    
    def __init__(self, *eventNames:str):
        """
        Constructs an event dispatcher instance with no events.
        """
        
        self.handlers = self._createEvents(*eventNames)

    def _createEvents(self, *eventNames:str) -> dict:
        """
        Creates the requested events in the event dispatcher registry.
        """

        temp = {}
        for event in eventNames:
            temp[event] = []

        return temp

    def subscribeToEvent(self, eventName:str, method):
        """
        Adds the passed handler method to the passed event.
        """
        self.handlers[eventName].append(method)
        pass

    def raiseEvent(self, eventName:str):
        """
        Raises the requested event.
        """

        if eventName in self.handlers:
            for handler in self.handlers[eventName]:
                handler()
        
        pass