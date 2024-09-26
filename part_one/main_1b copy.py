from models.KeyWordMatching import KeywordMatchingModel
from models.LogisticRegression import LogisticRegressionModel
from functions import datacleaning, vectorize
from sklearn.feature_extraction.text import TfidfVectorizer
import random
import pickle


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
        if distance <= 3:
            closest_matches.append((option, distance))
    
    if closest_matches:
        min_distance = min(closest_matches, key=lambda x: x[1])[1]
        best_matches = [match for match, dist in closest_matches if dist == min_distance]
        return random.choice(best_matches)

    return None # No match with word from db


def extract_preferences(user_utterence_input):
    """
    Functions to look for keywords that represents a type of cuisine, a location or a
    price range.
    """

    # Remove stop words from utterence
    # TO-DO
    
    preferences_dict = {"cuisine": "empty",
                        "location": "empty",
                        "pricerange": "empty"}

    words = user_utterence_input.split()

    # Alle opties uit database voor cuisine, loca en prijs
    db_cuisine = {"world", "Swedish", "Tuscan", "international", "Chinese", "Persian", "Cuban"}
    db_location = {"north", "south", "west", "east", "center"}
    db_pricerange = {"cheap", "moderate", "expensive"}

    # Keyword matching
    for word in words:

        if word in db_cuisine:
            preferences_dict["cuisine"] = word
        elif word in db_location:
            preferences_dict["location"] = word
        elif word in db_pricerange:
            preferences_dict["pricerange"] = word
    
        # If no exact match, check for closest match
        else:
            closest_match = Levenshtein_matching(word.lower(), db_cuisine)
            if closest_match:
                preferences_dict["cuisine"] = closest_match
                continue 

            closest_match = Levenshtein_matching(word.lower(), db_location)
            if closest_match:
                preferences_dict["location"] = closest_match
                continue

            closest_match = Levenshtein_matching(word.lower(), db_pricerange)
            if closest_match:
                preferences_dict["pricerange"] = closest_match
                continue

    # 'dontcare'???? 'any' + area/price/location
    # TO DO!

    return preferences_dict


# Example dialog simulation -------------------------------------------------------------
def run_dialog(model, vectorizer, initial_state):

    # Example of using the state transitions
    current_state = initial_state
    print(f"Current state: {current_state.name}")
    print(f"System: {current_state.message}")

    while current_state.name != "End":
        # Ask user for input
        user_input = input("User: ")
        print('-----------------------------------------------------------')
        print('-----------------------------------------------------------')
        # Fit and transform the training data
        print(user_input)

        vectorized_user_input = vectorizer.transform([user_input])

        print(vectorized_user_input)
        print('-----------------------------------------------------------')
        dialog_act = model.predict(vectorized_user_input)
        
        print(f"User dialog act: {dialog_act}")


        # Simulate a transition
        print('-----------------------------------------------------------')
        current_state = current_state.next_state(dialog_act[0])
        print('-----------------------------------------------------------')

        print(f"Next state: {current_state.name}")
        print('-----------------------------------------------------------')

        print(f"System: {current_state.message}")


def main():
    # Load the trained logistic regression model
    with open(r'part_one/trained_models/lr_model.pkl', 'rb') as f:
        model = pickle.load(f)
        
    with open(r'part_one/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    # Create states
    welcome_state = State("Welcome", "Welcome to the dialog system.")
    ask_area_state = State("Ask_area", "In what area would you like to eat?")
    end_state = State("End", "The conversation has ended.")

    # Add transitions
    welcome_state.add_transition("inform", ask_area_state)
    ask_area_state.add_transition("request", end_state) 

    print("Welcome to the dialog system.")
    run_dialog(model, vectorizer, welcome_state)

    

main()