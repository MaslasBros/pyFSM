class EventDispatcher:
    """
    Simple implementation of an event dispatcher to handle FSM events.
    """
    
    def __init__(self, *eventNames:str):
        """
        Constructs an event dispatcher instance with no events.

        Args:
            eventNames:
        """
        
        self.handlers = self._createEvents(*eventNames)
        """The event handlers"""

    def _createEvents(self, *eventNames:str) -> dict:
        """
        Creates the requested events in the event dispatcher registry.

        Args:
            eventNames (:class:`str`): The event names
        """

        temp = {}
        for event in eventNames:
            temp[event] = []

        return temp

    def subscribeToEvent(self, eventName:str, *method):
        """
        Adds the passed handler methods to the passed event.

        Args:
            eventName (:class:`str`): The event name
            method (:class:`func`): The method to add to this event
        """

        for func in method:
            self.handlers[eventName].append(func)
        pass

    def raiseEvent(self, eventName:str):
        """
        Raises the requested event.

        Args:
            eventName (:class:`str`): The event name.
        """

        if eventName in self.handlers:
            for handler in self.handlers[eventName]:
                handler()
        
        pass