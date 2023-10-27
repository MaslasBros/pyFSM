import FSM

@state
def idle():
    pass

@transition
def loading():
    pass

@state
def aim():
    pass

@state
def shoot():
    pass

@transition
def aiming():
    pass


_state_(idle(), loading(), aim())
_state_(aim(), aiming(), shoot())
_state_(shoot(), idle())
_state_(aiming(), idle())
_state_(aim(), idle(), shoot())