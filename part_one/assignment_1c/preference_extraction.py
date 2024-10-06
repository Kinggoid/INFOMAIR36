import re
from utils import Levenshtein_matching

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
        elif (word == 'food' or word =='restaurant') and preferences_dict["food type"] == None:
            
            # Option 1: "serving"/"for" + preference + "food"
            if i - 2 >= 0 and (words[i-2].startswith("serv") or words[i-2] == "for"):
                preferences_dict["food type"] = words[i-1]

            # Option 2: nationality ending with -ish or -an + "food"
            elif i-1 >= 0 and (words[i-1].endswith("ish") or words[i-1].endswith("an")):
                preferences_dict["food type"] = words[i-1]

    # If all preferences are 'dontcare', set them to 'dontcare'
    if all(value == 'dontcare' for value in preferences_dict.values()):
        preferences_dict = {key: 'dontcare' for key in preferences_dict}
    print(preferences_dict)
    return preferences_dict