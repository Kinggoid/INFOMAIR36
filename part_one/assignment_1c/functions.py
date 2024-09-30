import random
import re
import pandas as pd
from Levenshtein import distance as levenshtein_distance

def Levenshtein_matching(word, options, levenshtein_distance=3):
    closest_matches = []
    for option in options:
        dist = levenshtein_distance(word, option)
        if dist < threshold:
            closest_matches.append((option, dist))
    
    if closest_matches:
        min_distance = min(closest_matches, key=lambda x: x[1])[1]
        best_matches = [match for match, dist in closest_matches if dist == min_distance]
        return random.choice(best_matches)

    return None # No match with word from db


def extract_preferences(user_utterence_input, db_areas, db_cuisine, db_pricerange, threshold=3):
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

    preferences_dict = {"food type": None,
                        "area": None,
                        "pricerange": None}

    # Predefined 'dontcare' signaling words + area/food/price specification words
    dontcare_signal = {'any', 'whatever', "dontcare", "doesntmatter", "anywhere", "rest"}
    location_signal = {"area", "location", "part", "place", "town"}
    cuisine_signal = {"food", "cuisine", "type", "restaurant", "eat", "serves"}
    pricerange_signal = {"price", "cost", "budget"}

    # Go through the sentence(s)
    for i, word in enumerate(words):

        # Keyword matching
        if word in db_cuisine:
            preferences_dict["food type"] = word
        elif word in db_areas:
            preferences_dict["area"] = word
        elif word in db_pricerange:
            preferences_dict["pricerange"] = word
        
        # Check for 'dontcare' preference value
        elif word in dontcare_signal:
            # Match with preference context
            window = words[max(0, i - 3):i + 3]

            if any(kw in window for kw in location_signal):
                preferences_dict["area"] = 'dontcare'
            elif any(kw in window for kw in cuisine_signal):
                preferences_dict["food type"] = 'dontcare'
            elif any(kw in window for kw in pricerange_signal):
                preferences_dict["pricerange"] = 'dontcare'
            else:
                preferences_dict["undefined_context"] = 'dontcare'

        # If no exact match, check for closest match
        elif len(word) > 4:        # Only 'longer' words bc otherwise filter is too broad
            closest_match = Levenshtein_matching(word.lower(), db_cuisine, threshold=threshold)
            if closest_match:
                if preferences_dict["food type"] == None: # Only fill up when no other value saved: 'west part of town'
                    preferences_dict["food type"] = closest_match
                    continue 

            closest_match = Levenshtein_matching(word.lower(), db_areas, threshold=threshold)
            if closest_match:
                if preferences_dict["area"] == None:
                    preferences_dict["area"] = closest_match
                    continue

            closest_match = Levenshtein_matching(word.lower(), db_pricerange, threshold=threshold)
            if closest_match:
                if preferences_dict["pricerange"] == None:
                    preferences_dict["pricerange"] = closest_match
                    continue

        # Final check: possible unrecognized foodtype preference missed?
        elif word == 'food' and preferences_dict["food type"] == None:
            
            # Option 1: "serving"/"for" + preference + "food"
            if i - 2 > 0 and (words[i-2].startswith("serv") or words[i-2] == "for"):
                preferences_dict["food type"] = words[i-1]

            # Option 2: nationality ending with -ish or -an + "food"
            elif i-1 > 0 and (words[i-1].endswith("ish") or words[i-1].endswith("an")):
                preferences_dict["food type"] = words[i-1]

    return preferences_dict


def lookup(restaurant_df, preferences_dict):
    """
    Filter the DataFrame based on the preferences and return the filtered DataFrame.
    """

    # Apply filters based on preferences
    if preferences_dict["pricerange"] is not None:
        restaurant_df = restaurant_df[restaurant_df["pricerange"].str.lower() == preferences_dict["pricerange"].lower()]
    
    if preferences_dict["area"] is not None:
        restaurant_df = restaurant_df[restaurant_df["area"].str.lower() == preferences_dict["area"].lower()]
    
    if preferences_dict["food type"] is not None:
        restaurant_df = restaurant_df[restaurant_df["food"].str.lower() == preferences_dict["food type"].lower()]

    return restaurant_df


def ask_preferences(user_input, preferences_dict, unique_areas, unique_foodtype, unique_pricerange, restaurant_df):
    new_preferences = extract_preferences(user_input, unique_areas, unique_foodtype, unique_pricerange)

    # Update the existing preferences_dict
    for key, value in new_preferences.items():
        if value is not None:
            preferences_dict[key] = value

    missing_preferences = [pref for pref, value in preferences_dict.items() if value is None]

    available_restaurants = lookup(restaurant_df, preferences_dict)
    if available_restaurants.empty:
        print(f"System: I am sorry, there are no restaurants with those preferences: "
              f"Area: {preferences_dict['area']}, "
              f"Food Type: {preferences_dict['food type']}, "
              f"Price Range: {preferences_dict['pricerange']}. "
              "Please provide me with different preferences.")
        return "preference_doesnt_exist", available_restaurants
    elif not missing_preferences:
        # Suggest the first restaurant from the filtered DataFrame
        suggest_restaurant(available_restaurants)
        return "suggest_restaurant", available_restaurants
    elif "area" in missing_preferences:
        print("System: In what area would you like to eat?")
        return "ask_area", available_restaurants
    elif "food type" in missing_preferences:
        print("System: What type of food are you looking for?")	
        return "ask_food_type", available_restaurants
    elif "pricerange" in missing_preferences:
        print("System: What type of price range are you looking for?")
        return "ask_price_range", available_restaurants
    else:
        print('For testing. If you read this, something went wrong')
        return None, available_restaurants


def suggest_restaurant(available_restaurants):
    suggested_restaurant = available_restaurants.iloc[0]
    
    # Extract details of the suggested restaurant
    restaurant_name = suggested_restaurant['restaurantname']
    restaurant_food = suggested_restaurant['food']
    restaurant_area = suggested_restaurant['area']
    restaurant_pricerange = suggested_restaurant['pricerange']
    
    # Print the suggestion
    print(f"System: I suggest {restaurant_name}. It serves {restaurant_food} food in the {restaurant_area} area and falls within the {restaurant_pricerange} price range.")


