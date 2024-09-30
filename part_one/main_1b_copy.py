from models.KeyWordMatching import KeywordMatchingModel
from models.LogisticRegression import LogisticRegressionModel
from functions import datacleaning, vectorize
from sklearn.feature_extraction.text import TfidfVectorizer
import random
import Levenshtein
import random
import pandas as pd
import numpy as np
import re

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

# Identify user preference statements ---------------------------------------------------

def Levenshtein_matching(word, options):

    closest_matches = []
    for option in options:
        distance = Levenshtein.distance(word, option)
        if distance < 3:
            closest_matches.append((option, distance))
    
    if closest_matches:
        min_distance = min(closest_matches, key=lambda x: x[1])[1]
        best_matches = [match for match, dist in closest_matches if dist == min_distance]
        return random.choice(best_matches)

    return None # No match with word from db


def extract_preferences(user_utterence_input):
    """
    Functions to look for keywords that represents a type of cuisine, a location or a
    price range. Outputs a dictionary with the extracted information.
    """

    # Clean up
    user_utterence_input = re.sub(r'[^\w\s]', '', user_utterence_input)
    words = user_utterence_input.split()

    # Glue doesntmatter & dontcare together to be recognized for 'dontcare' label
    final_words = []
    skip_next_word = 0

    for i, word in enumerate(words):
        
        # Skip the next word after word-combo has already been added to copy words
        if skip_next_word == 1:
            # Reset
            skip_next_word = 0
            continue
        
        # Loop through sentence and make an adjusted copy
        if word == "dont" and words[i+1] == "care" and i+1<len(words):
            final_words.append("dontcare")
            skip_next_word = 1
        elif word == "doesnt" and words[i+1] == "matter" and i+1<len(words):
            final_words.append("doesntmatter")
            skip_next_word = 1
        else:
            final_words.append(word)

    words = final_words

    # Remove stop words from utterence
    stopwords = {"i", "am", "looking", "for", "a", "an", "the", "in", "to", "of", "is",
                 "and", "on", "that", "please", "with", "find", "it"}
    words = [word.lower() for word in words if word.lower() not in stopwords]

    preferences_dict = {"cuisine": "empty",
                        "location": "empty",
                        "pricerange": "empty"}

    # Save all the options for typefood, area and location
    df = pd.read_csv('part_one\\restaurant_info.csv')
    db_pricerange = set(df['pricerange'].dropna().str.lower())
    db_areas = set(df['area'].dropna().str.lower())
    db_cuisine = set(df['food'].dropna().str.lower())

    # Predefined 'dontcare' signaling words + area/food/price specification words
    dontcare_signal = {'any', 'whatever', "dontcare", "doesntmatter", "anywhere", "rest"}
    location_signal = {"area", "location", "part", "place", "town"}
    cuisine_signal = {"food", "cuisine", "type", "restaurant", "eat", "serves"}
    pricerange_signal = {"price", "cost", "budget"}

    # Go through the sentence(s)
    for i, word in enumerate(words):

        # Keyword matching
        if word in db_cuisine:
            preferences_dict["cuisine"] = word
        elif word in db_areas:
            preferences_dict["location"] = word
        elif word in db_pricerange:
            preferences_dict["pricerange"] = word
        
        # Check for 'dontcare' preference value
        elif word in dontcare_signal:
            # Match with preference context
            window = words[max(0, i - 3):i + 3]

            if any(kw in window for kw in location_signal):
                preferences_dict["location"] = 'dontcare'
            elif any(kw in window for kw in cuisine_signal):
                preferences_dict["cuisine"] = 'dontcare'
            elif any(kw in window for kw in pricerange_signal):
                preferences_dict["pricerange"] = 'dontcare'
            else:
                preferences_dict["undefined_context"] = 'dontcare'

        # If no exact match, check for closest match
        elif len(word) > 4:        # Only 'longer' words bc otherwise filter is too broad
            closest_match = Levenshtein_matching(word.lower(), db_cuisine)
            if closest_match:
                if preferences_dict["cuisine"] == "empty": # Only fill up when no other value saved: 'west part of town'
                    preferences_dict["cuisine"] = closest_match
                    continue 

            closest_match = Levenshtein_matching(word.lower(), db_areas)
            if closest_match:
                if preferences_dict["location"] == "empty":
                    preferences_dict["location"] = closest_match
                    continue

            closest_match = Levenshtein_matching(word.lower(), db_pricerange)
            if closest_match:
                if preferences_dict["pricerange"] == "empty":
                    preferences_dict["pricerange"] = closest_match
                    continue

        # Final check: possible unrecognized foodtype preference missed?
        elif word == 'food' and preferences_dict["cuisine"] == "empty":
            
            # Option 1: "serving"/"for" + preference + "food"
            if i - 2 > 0 and (words[i-2].startswith("serv") or words[i-2] == "for"):
                preferences_dict["cuisine"] = words[i-1]

            # Option 2: nationality ending with -ish or -an + "food"
            elif i-1 > 0 and (words[i-1].endswith("ish") or words[i-1].endswith("an")):
                preferences_dict["cuisine"] = words[i-1]

    return preferences_dict


# Function to retrieve restaurant suggestions from CSV file -----------------------------
def lookup(preferences):
    """
    Function that takes the preference dictionary (stating cuisine, area and pricerange
    preferences) and loops through the restaurant_info.csv file to find possible restaurants.
    These names are saved in a list and given as output.
    NOTE: Needs fully filled preference dict (doesn't deal with empty values)
    """

    # Read CSV
    df = pd.read_csv('part_one\\restaurant_info.csv')
    list_of_possible_restaurants = []

    # Filter restaurants by food, area and pricerange
    if preferences["cuisine"] != "dontcare":
        df = df[df["food"].str.lower() == preferences["cuisine"]]

    if preferences["location"] != "dontcare":
        df = df[df["area"].str.lower() == preferences["location"]]

    if preferences["pricerange"] != "dontcare":
        df = df[df["pricerange"].str.lower() == preferences["pricerange"]]

    # Save names to list
    list_of_possible_restaurants = df["restaurantname"].tolist()

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
        user_input = user_input.split()
        print('-----------------------------------------------------------')
        vectorizer = TfidfVectorizer()
        print('-----------------------------------------------------------')
        # Fit and transform the training data
        print(user_input)
        # vectorized_user_input = vectorizer.fit_transform(user_input)

        # print(vectorized_user_input)
        print('-----------------------------------------------------------')
        dialog_act = model.predict(user_input)
        
        print(f"User dialog act: {dialog_act}")


        # Simulate a transition
        current_state = current_state.next_state(dialog_act)
        print(f"Next state: {current_state.name}")
        print(f"System: {current_state.message}")



def main():
    file_path = 'part_one\\dialog_acts.dat'
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

    print("Welcome to the dialog system.")
    run_dialog(model, welcome_state)

    

# main()

# Testing extract preferences function: ----------------------------------------------
# (Jennifer)

user_input = "I'm looking for world food"
user_input= "I want a restaurant that serves world food"
user_input= "I want a restaurant serving Swedish food"
# user_input= "I'm looking for a restaurant in the center" # Check
# user_input= "I would like a cheap restaurant in the west part of town" # Check
# user_input= "I'm looking for a moderately priced restaurant in the west part of town" # Check
# user_input= "I'm looking for a restaurant in any area that serves Tuscan food" # Check
# user_input= "Can I have an expensive restaurant" # Check
# user_input= "I'm looking for an expensive restaurant and it should serve international food" # Check
# user_input= "I need a Cuban restaurant that is moderately priced" # Check
# user_input= "I'm looking for a moderately priced restaurant with Catalan food" # Check
# user_input= "What is a cheap restaurant in the south part of town" # Check
# user_input= "What about Chinese food" # Check
# user_input= "I wanna find a cheap restaurant" # Check
# user_input= "I'm looking for Persian food please" # Check
# user_input= "Find a Cuban restaurant in the center" # Check
# user_input = "I don't care"

preference_dict = extract_preferences(user_input)
print(preference_dict)

possible_restaurants = lookup(preference_dict)
print(possible_restaurants)