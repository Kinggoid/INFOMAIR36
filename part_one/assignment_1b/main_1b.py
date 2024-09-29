import random
import pickle
import re
import pandas as pd
import Levenshtein
from state import State
from state_diagram import State_diagram
from functions import *
import sys
import os
import pickle

def main():
    # Load the trained logistic regression model
    with open(r'part_one/trained_models/lr_model.pkl', 'rb') as f:
        model = pickle.load(f)
        
    with open(r'part_one/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    # Create states
    welcome_state = State("Welcome", "Welcome to the dialog system.")
    ask_area_state = State("Ask_area", "In what area would you like to eat?")
    ask_food_state = State("Ask_food", "What type of food are you looking for?")
    ask_price_state = State("Ask_price", "What type of price range are you looking for?")
    double_check_state = State("Double_check","So you want to eat at VAR place?")
    no_match_state = State("No_match", "Sorry, such a restaurant does not exist")
    suggest_restaurant_state = State("Suggest_restaurant", "VAR is a nice restaurant to eat at")
    give_info_state = State("Give_info", "The info for this restaurant is VAR")
    end_state = State("End", "The conversation has ended.")

    # Add transitions
    welcome_state.add_transition("inform", ask_area_state)
    welcome_state.add_transition("null", ask_area_state)
    welcome_state.add_text("Welkom, ga verder")

    ask_area_state.add_transition("infomr", ask_food_state)

    ask_food_state.add_transition("INFORM", ask_price_state)

    ask_price_state.add_transition("INFORM", double_check_state)

    double_check_state.add_transition("CONFIRM", suggest_restaurant_state)

    double_check_state.add_transition("DENY", no_match_state)

    suggest_restaurant_state.add_transition("INFORM", give_info_state)
    suggest_restaurant_state.add_text()

    give_info_state.add_transition("INFORM", end_state)

    # Add state diagram
    state_diagram = State_diagram()

    #welcoming user 
    print(f"Current state: {welcome_state.name}")
    print(f"System: {welcome_state.message}")

    #setting current state
    current_state = welcome_state

    #iterate until you reach the end state
    while current_state.name != "End":
        #getting user input
        user_input = input("User: ")
        #vectorizing input to use for ML model
        vectorized_user_input = vectorizer.transform([user_input])
        #classifying user input using ML model
        dialog_act = model.predict(vectorized_user_input)
        #print dialog_act
        print(f"User dialog act: {dialog_act}")

        #get upcoming state
        current_state = state_transition_function(current_state, user_input, dialog_act)
        print(f"System: {current_state.message}")


if __name__ == "__main__":
    main()