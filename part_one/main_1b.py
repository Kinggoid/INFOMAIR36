import numpy as np
import pandas as pd
from part_one.models.KeyWordMatching import KeywordMatchingModel
from part_one.models.majority_class import MajorityClassModel

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
def state_transition_function(current_dialog_state, user_input):
    
    print(f"System dialog state: {current_dialog_state}")
    
    # 1. Convert user input to lower case
    user_input = user_input.lower()

    # 2. Classify input (classifier 1a) >> TO-DO later
    dialog_act = KeywordMatchingModel(user_input)
    dialog_act = "hello"

    # 3. Update dialogstate and decide system output (as in state transition diagram!)
    next_state = current_dialog_state
    system_response = ""

    if current_dialog_state == DialogState.WELCOME:

        if dialog_act == DialogAct.HELLO:
            next_state = DialogState.ASK_AREA
            system_response = "In what area would you like to eat?"

    elif current_dialog_state == DialogState.ASK_AREA:
        print("State switch to dialogState = ASK_AREA")
        if dialog_act == DialogAct.INFORM:
            next_state = DialogState.END
            system_response = "Thank you!"

        elif dialog_act == DialogAct.REQUEST:
            next_state = DialogState.PROVIDE_INFO
            system_response = "What information would you like to know?"
    
    elif current_dialog_state == DialogState.END:
        system_response = "The conversation has ended."

    return next_state, system_response

# Identify user preference statements ---------------------------------------------------
def extract_preferences(input):

    # 16 examples have to work
    # use keyword matching algorithm
    # python-levenshtein

    return 

# Function to retrieve restaurant suggestions from CSV file -----------------------------
def lookup(preferences):
    list_of_possible_restaurants = []
    return list_of_possible_restaurants

# Example dialog simulation -------------------------------------------------------------
def run_dialog():
    current_dialog_state = DialogState.WELCOME
    print("System: Welcome to the dialog system.")
    
    while current_dialog_state != DialogState.END:

        # 1. ACCEPT USER INPUT
        user_input = input("User: ")
        
        # 2. CLASSIFY INPUT & MAKE STATE TRANSITION
        next_dialog_state, associated_system_utterence = state_transition_function(current_dialog_state, user_input)

        # (update)
        current_dialog_state = next_dialog_state
                
        # 3. PRINT SYSTEM RESPONSE
        print(f"System: {associated_system_utterence}")

# Run the dialog
run_dialog()

