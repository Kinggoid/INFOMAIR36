import random
import pickle
import re
import pandas as pd
import Levenshtein

########## not worked out yet ##############
class state_diagram:
    def __init__(self, states):
        self.area = None
        self.food = None
        self.price = None


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


# Identify user preference statements ---------------------------------------------------

def Levenshtein_matching(word: str, options: list, threshold: int = 3) -> str:
    """
    Finds the closest match for a word from a list of options using Levenshtein distance.

    Parameters:
    word (str): The word to match.
    options (list): A list of possible options.
    threshold (int): The maximum distance to consider a match. Default is 3.

    Returns:
    str: The closest matching word from the options, or None if no match is found within the threshold.
    """
    closest_matches = []
    distances = []

    for option in options:
        distance = Levenshtein.distance(word, option)
        if distance <= threshold:
            closest_matches.append(option)
            distances.append(distance)
    
    if closest_matches:
        min_distance = min(closest_matches, key=lambda x: x[1])[1]
        best_matches = [match for match, dist in closest_matches if dist == min_distance]
        return random.choice(best_matches)

    return None  # No match with word from db


def extract_preferences(user_utterence_input):
    """
    Functions to look for keywords that represents a type of cuisine, a location or a
    price range. Outputs a dictionary with the extracted information.
    """

    # Clean up
    user_utterence_input = re.sub(r'[^\w\s]', '', user_utterence_input)
    words = user_utterence_input.split()

    # TO-DO: "don't care" >> turn into one word or something else

    # Remove stop words from utterence
    stopwords = {"i", "am", "looking", "for", "a", "an", "the", "in", "to", "of", "is",
                 "and", "on", "that", "please", "with", "find", "it"}
    words = [word.lower() for word in words if word.lower() not in stopwords]
    
    preferences_dict = {"location": "empty",
                        "cuisine": "empty",
                        "pricerange": "empty"}

    # Save all the options for typefood, area and location
    df = pd.read_csv('part_one\\restaurant_info.csv')
    db_pricerange = set(df['pricerange'].dropna().str.lower())
    db_areas = set(df['area'].dropna().str.lower())
    db_cuisine = set(df['food'].dropna().str.lower())

    # Predefined 'dontcare' signaling words + area/food/price specification words
    dontcare_signal = {'any', 'whatever', "dontcare"}
    location_signal = {"area", "location", "part", "place", "town"}
    cuisine_signal = {"food", "cuisine", "type", "restaurant", "eat", "serves"}
    pricerange_signal = {"price", "cost", "budget"}

    # Go through the sentence(s)
    for i, word in enumerate(words):

        # TO-DO: what to do with 'world'/ 'Swedish'
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
            print(window)

            if any(kw in window for kw in location_signal):
                preferences_dict["location"] = 'dontcare'
            elif any(kw in window for kw in cuisine_signal):
                preferences_dict["cuisine"] = 'dontcare'
            elif any(kw in window for kw in pricerange_signal):
                preferences_dict["pricerange"] = 'dontcare'
            else:
                preferences_dict["undefined_context"] = 'dontcare'

        # If no exact match, check for closest match
        elif word != 'want':        # TO-DO: 'part'/'want' turns into 'east'or 'west' with Levenshtein
            closest_match = Levenshtein_matching(word.lower(), db_cuisine)
            if closest_match:
                print(word, closest_match)
                preferences_dict["cuisine"] = closest_match
                continue 

            closest_match = Levenshtein_matching(word.lower(), db_areas)
            if closest_match:
                print(word, closest_match)
                preferences_dict["location"] = closest_match
                continue

            closest_match = Levenshtein_matching(word.lower(), db_pricerange)
            if closest_match:
                print(word, closest_match)
                preferences_dict["pricerange"] = closest_match
                continue
        
    return preferences_dict


# Function to retrieve restaurant suggestions from CSV file -----------------------------
def lookup(preferences):
    """
    Function that takes the preference dictionary (stating cuisine, area and pricerange
    preferences) and loops through the restaurant_info.csv file to find possible restaurants.
    These names are saved in a list and given as output.
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

    # NOTE: dealt nog niet met 'empty', ergens anders wann 'dontcare' veranderen in dict

    # Save names to list
    list_of_possible_restaurants = df["restaurantname"].tolist()

    return list_of_possible_restaurants


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




main()