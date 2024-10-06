import random
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
