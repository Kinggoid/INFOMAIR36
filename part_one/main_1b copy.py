from models.KeyWordMatching import KeywordMatchingModel
from models.majority_class import MajorityClassModel


class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}
    
    def add_transition(self, input, next_state):
        self.transitions[input] = next_state
    
    def next_state(self, input):
        if input in self.transitions:
            return self.transitions[input]
        else:
            return self


# Define states
class DialogState:
    WELCOME = 'WELCOME'
    ASK_AREA = 'ASK_AREA'
    ASK_FOODTYPE = 'ASK_FOODTYPE'
    ASK_PRICERANGE = 'ASK_PRICERANGE'
    RECEIVE_PREFERENCES = 'RECEIVE_PREFERENCES'
    PROVIDE_RESTAURANT = 'PROVIDE_RESTAURANT'
    NO_RESTAURANT = 'NO_RESTAURANT'
    PROVIDE_CONTACT = 'PROVIDE_CONTACT'
    END = 'END'

# Dialog acts (classified inputs of the user)
class DialogAct:
    ACK = 'acknowledgement' # Okay uhm
    AFFIRM = 'positive conformation' # Yes right
    BYE = 'greeting at the end of the dialog' # See you good bye
    CONFIRM = 'check if given information confirms to query' # Is is in the center of town
    DENY = 'reject system suggestion' # I don't want Vietnamese food
    HELLO = 'hello' # Hi I want a restaurant
    INFORM = 'state a preference or other information' # I'm looking for a restaurant that serves seafood
    NEGATE = 'negation' # No in any area
    NULL = 'noise or utterance without content' # Cough
    REPEAT = 'ask for repetition' # Can you repeat that
    REQALTS = 'request alternative suggestions' # How about Korean food
    REQMORE = 'request more suggestions' # More
    REQUEST = 'ask for information' # What is the post code
    RESTART = 'attempt to restart the dialog' # Okay start over
    THANKYOU = 'express thanks' # Thank you good bye

# STATE TRANSITION FUNCTION: ----------------------------------------------------------
def state_transition_function(current_state, user_input):
    
    print(f"System dialog state: {current_state.name}")
    
    # 1. Convert user input to lower case
    user_input = user_input.lower()

    # 2. Classify input (classifier 1a) >> TO-DO later
    dialog_act = KeywordMatchingModel(user_input)
    dialog_act = "hello"

    # 3. Update dialogstate and decide system output (as in state transition diagram!)
    next_state = current_state.next_state(dialog_act)
    system_response = ""

    if current_state.name == DialogState.WELCOME:
        if dialog_act == DialogAct.HELLO:
            system_response = "In what area would you like to eat?"

    elif current_state.name == DialogState.ASK_AREA:
        print("State switch to dialogState = ASK_AREA")
        if dialog_act == DialogAct.INFORM:
            system_response = "Thank you!"
        elif dialog_act == DialogAct.REQUEST:
            system_response = "What information would you like to know?"
    
    elif current_state.name == DialogState.END:
        system_response = "The conversation has ended."

    return next_state, system_response

# Example dialog simulation -------------------------------------------------------------
def run_dialog(initial_state):
    current_state = initial_state
    print("System: Welcome to the dialog system.")
    
    while current_state.name != DialogState.END:

        # 1. ACCEPT USER INPUT
        user_input = input("User: ")
        
        # 2. CLASSIFY INPUT & MAKE STATE TRANSITION
        next_state, associated_system_utterance = state_transition_function(current_state, user_input)

        # (update)
        current_state = next_state
                
        # 3. PRINT SYSTEM RESPONSE
        print(f"System: {associated_system_utterance}")

def main():
    # Create states
    welcome_state = State(DialogState.WELCOME)
    ask_area_state = State(DialogState.ASK_AREA)
    end_state = State(DialogState.END)

    # Add transitions
    welcome_state.add_transition(DialogAct.HELLO, ask_area_state)
    ask_area_state.add_transition(DialogAct.INFORM, end_state)
    ask_area_state.add_transition(DialogAct.REQUEST, end_state)  # Assuming REQUEST leads to END for simplicity

    # Example of using the state transitions
    current_state = welcome_state
    print(f"Current state: {current_state.name}")

    # Simulate a transition
    user_input = DialogAct.HELLO
    current_state = current_state.next_state(user_input)
    print(f"Next state: {current_state.name}")

    user_input = DialogAct.INFORM
    current_state = current_state.next_state(user_input)
    print(f"Next state: {current_state.name}")

    # Run the dialog
    run_dialog(welcome_state)

main()