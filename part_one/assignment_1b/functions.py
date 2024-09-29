import random
import re
import pandas as pd
from Levenshtein import distance as Levenshtein


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