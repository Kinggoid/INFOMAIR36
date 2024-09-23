from models.KeyWordMatching import KeywordMatchingModel
from models.LogisticRegression import LogisticRegressionModel
from functions import datacleaning, vectorize


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

def lookup(preferences):
    list_of_possible_restaurants = []
    return list_of_possible_restaurants


# Example dialog simulation -------------------------------------------------------------
def run_dialog(model, initial_state):
    # Example of using the state transitions
    current_state = initial_state
    print(f"Current state: {current_state.name}")
    print(f"System: {current_state.message}")

    while current_state.name != "End":
        # Ask user for input
        user_input = input("User: ")
        print('-----------------------------------------------------------')
        dialog_act = model.predict(user_input)
        
        print(f"User dialog act: {dialog_act}")


        # Simulate a transition
        current_state = current_state.next_state(dialog_act)
        print(f"Next state: {current_state.name}")
        print(f"System: {current_state.message}")



def main():
    file_path = 'part_one\dialog_acts.dat'
    X_train, X_test, y_train, y_test = datacleaning(file_path)

    X_train, X_test = vectorize(X_train, X_test)

    model = LogisticRegressionModel()
    model.fit(X_train, y_train)

    # Create states
    welcome_state = State("Welcome", "Welcome to the dialog system.")
    ask_area_state = State("Ask_area", "In what area would you like to eat?")
    end_state = State("End", "The conversation has ended.")

    # Add transitions
    welcome_state.add_transition("INFORM", ask_area_state)
    ask_area_state.add_transition("REQUEST", end_state) 

    run_dialog(model, welcome_state)

    

main()