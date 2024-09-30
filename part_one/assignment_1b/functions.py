import random
import re
import pandas as pd
from Levenshtein import distance as Levenshtein


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
    print(words)

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
        elif len(word) > 4:        # Only 'longer' words bc otherwise filter is too broad
            closest_match = Levenshtein_matching(word.lower(), db_cuisine)
            if closest_match:
                print(word, closest_match)
                if preferences_dict["cuisine"] == "empty": # Only fill up when no other value saved: 'west part of town'
                    preferences_dict["cuisine"] = closest_match
                    continue 

            closest_match = Levenshtein_matching(word.lower(), db_areas)
            if closest_match:
                print(word, closest_match)
                if preferences_dict["location"] == "empty":
                    preferences_dict["location"] = closest_match
                    continue

            closest_match = Levenshtein_matching(word.lower(), db_pricerange)
            if closest_match:
                print(word, closest_match)
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
def lookup(food, pricerange, area):

    """
    Function that takes the preference dictionary (stating cuisine, area and pricerange
    preferences) and loops through the restaurant_info.csv file to find possible restaurants.
    These names are saved in a list and given as output.
    """

    # Read CSV
    df = pd.read_csv('part_one/data/restaurant_info.csv')
    list_of_possible_restaurants = []

    # Filter restaurants by food, area and pricerange
    if food != "dontcare":
        df = df[df["food"].str.lower() == food]

    if area != "dontcare":
        df = df[df["area"].str.lower() == area]

    if pricerange != "dontcare":
        df = df[df["pricerange"].str.lower() == pricerange]

    # NOTE: dealt nog niet met 'empty', ergens anders wann 'dontcare' veranderen in dict

    # Save names to list
    list_of_possible_restaurants = df["restaurantname"].tolist()

    return list_of_possible_restaurants


# Function to recommend a restaurant
def recommend_restaurant(food, pricerange, area):
    filtered_restaurants = lookup(food, pricerange, area)

    if filtered_restaurants.empty:
        return "I am sorry, but there are no restaurants matching your criteria.", None
    else:
        return filtered_restaurants
