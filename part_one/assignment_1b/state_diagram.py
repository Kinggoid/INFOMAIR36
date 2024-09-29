from state import State
from functions import *


class State_diagram:
    def __init__(self, states):
        self.area = None
        self.food = None
        self.price = None
        self.states = states
    
    def add_state(self, state):
        self.states.append(state)
    
    def get_state(self, state_name):
        for state in self.states:
            if state.name == state_name:
                return state
        return None
    
    def get_next_state(self, current_state, input):
        return self.get_state(current_state).next_state(input)
    
    # Example dialog simulation -------------------------------------------------------------
    def state_transition_function(initial_state, user_input, dialog_act):
        #show current state
        current_state = initial_state
        print(f"Current state: {current_state.name}")
        print(f"System: {current_state.message}")

        #only assign preference_dict if its an INFORM act
        if dialog_act == "INFORM":
            preference_dict = extract_preferences(user_input)

        #logic for state transitions
        if current_state == welcome_state:      # Go to ask_area state if you do not know where the user wants to eat
            if dialog_act == "INFORM":
                # extract preferences
                # save / overwrite preferences
                # go next state
                if preference_dict[0] == "empty":
                    current_state = ask_area_state
                    return ask_area_state
        elif current_state == ask_area_state:   # Go to ask_food_state if you do not know what food the user wants to eat
            if dialog_act == "INFORM":
                if preference_dict[1] == "empty":
                    current_state == ask_food_state
                    return current_state
        elif current_state == ask_food_state:   # Go to ask_price state if you do not know what price the user wants to pay
            if dialog_act == "INFORM":
                if preference_dict[2] == "empty":
                    current_state == ask_price_state
                    return current_state
