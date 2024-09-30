class State:
    def __init__(self, name, message):
        self.name = name
        self.lookup = None
        self.transitions = {}
        self.message = message
    
    def add_transition(self, input, next_state):
        self.transitions[input] = next_state
    
    def next_state(self, input):
        if input in self.transitions:
            return self.transitions[input]
        else:
            return self