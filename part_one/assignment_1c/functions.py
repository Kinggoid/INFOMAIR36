import random
import re
import pandas as pd
from Levenshtein import distance as levenshtein_distance

def Levenshtein_matching(word, options, threshold=3):
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


import re

def extract_preferences(user_utterance_input, db_areas, db_cuisine, db_pricerange, threshold=3):
    """
    Functions to look for keywords that represent a type of cuisine, a location, or a
    price range. Outputs a dictionary with the extracted information.
    """

    # Clean up
    user_utterance_input = re.sub(r'[^\w\s]', '', user_utterance_input)
    words = user_utterance_input.split()

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
        if word == "dont" and i+1 < len(words) and words[i+1] == "care":
            final_words.append("dontcare")
            skip_next_word = 1
        elif word == "doesnt" and i+1 < len(words) and words[i+1] == "matter":
            final_words.append("doesntmatter")
            skip_next_word = 1
        else:
            final_words.append(word)

    words = final_words

    # Remove stop words from utterance
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
            closest_match = Levenshtein_matching(word.lower(), db_cuisine, threshold)
            if closest_match:
                if preferences_dict["food type"] == None: # Only fill up when no other value saved: 'west part of town'
                    preferences_dict["food type"] = closest_match
                    continue 

            closest_match = Levenshtein_matching(word.lower(), db_areas, threshold)
            if closest_match:
                if preferences_dict["area"] == None:
                    preferences_dict["area"] = closest_match
                    continue

            closest_match = Levenshtein_matching(word.lower(), db_pricerange, threshold)
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

    # If all preferences are 'dontcare', set them to 'dontcare'
    if all(value == 'dontcare' for value in preferences_dict.values()):
        preferences_dict = {key: 'dontcare' for key in preferences_dict}

    return preferences_dict


def lookup(restaurant_df, preferences_dict):
    """
    Filter the DataFrame based on the preferences and return the filtered DataFrame.
    """

    # Apply filters based on preferences
    if preferences_dict["pricerange"] is not None and preferences_dict["pricerange"].lower() != "dontcare":
        restaurant_df = restaurant_df[restaurant_df["pricerange"].str.lower() == preferences_dict["pricerange"].lower()]
    
    if preferences_dict["area"] is not None and preferences_dict["area"].lower() != "dontcare":
        restaurant_df = restaurant_df[restaurant_df["area"].str.lower() == preferences_dict["area"].lower()]
    
    if preferences_dict["food type"] is not None and preferences_dict["food type"].lower() != "dontcare":
        restaurant_df = restaurant_df[restaurant_df["food"].str.lower() == preferences_dict["food type"].lower()]

    return restaurant_df


def suggest_restaurant(available_restaurants):
    suggested_restaurant = available_restaurants.iloc[0]
    
    # Extract details of the suggested restaurant
    restaurant_name = suggested_restaurant['restaurantname']
    restaurant_food = suggested_restaurant['food']
    restaurant_area = suggested_restaurant['area']
    restaurant_pricerange = suggested_restaurant['pricerange']
    
    # Print the suggestion
    print(f"System: I suggest {restaurant_name}. It serves {restaurant_food} food in the {restaurant_area} area and falls within the {restaurant_pricerange} price range.")

def add_reasoning_data(df):
    """
    Add reasoning data to the DataFrame.
    """
    food_quality_options = ["good", "not good"]
    crowdedness_options = ["busy", "not busy"]
    length_of_stay_options = ["long stay", "short stay"]
    
    food_quality_list = []
    crowdedness_list = []
    length_of_stay_list = []
    
    for i in range(len(df)):
        food_quality_list.append(random.choice(food_quality_options))
        crowdedness_list.append(random.choice(crowdedness_options))
        length_of_stay_list.append(random.choice(length_of_stay_options))
    
    df["food_quality"] = food_quality_list
    df['crowdedness'] = crowdedness_list
    df['length_of_stay'] = length_of_stay_list

    return df


def apply_inference_rules(restaurant_df, user_input):
    """
    output: restaurant_df with all restaurants that fit the additional_requirements
    """
    # Ensure user input is a string, convert to lowercase, remove non-alphanumeric characters, and split into words
    words = set(re.sub(r'[^\w\s]', '', str(user_input).lower()).split())

    # Define the additional requirements
    additional_req_signal = {"touristic", "assigned seats", "children", "romantic"}

    # Filter the matching requirements
    additional_requirements = [match for match in additional_req_signal if match in words]

    # Initialize an empty DataFrame to store the valid rows
    valid_restaurants_df = pd.DataFrame(columns=restaurant_df.columns)

    for _, row in restaurant_df.iterrows():
        print(row)
        # Extract necessary information from the row
        crowdedness = row.get("crowdedness", "").lower()
        food = row.get("food", "").lower()
        price = row.get("price", "").lower()
        stay_duration = row.get("length_of_stay", "").lower()
        food_quality = row.get("food_quality", "").lower()

        # Apply inference rules
        if "touristic" in additional_requirements:
            if food != "romanian" and price == "cheap" and food_quality == "good":  # This restaurant is touristic
                pass  
            else:
                continue 

        if "assigned seats" in additional_requirements:
            if crowdedness == "busy":  # This restaurant has assigned seats
                pass  
            else:
                continue 

        if "children" in additional_requirements:
            if stay_duration != "long":  # This restaurant is suitable for children
                pass  
            else:
                continue  

        if "romantic" in additional_requirements:
            if crowdedness != "busy" and stay_duration == "long":  # It is a romantic restaurant	
                pass  
            else:
                continue

        # If the row meets all requirements, add it to the new DataFrame
        valid_restaurants_df = pd.concat([valid_restaurants_df, pd.DataFrame([row])], ignore_index=True)

    # Reset the index of the new DataFrame
    valid_restaurants_df.reset_index(drop=True, inplace=True)

    return valid_restaurants_df