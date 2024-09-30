import pandas as pd
import numpy as np
import random
from assignment_1b.functions import extract_preferences, lookup
import re


restaurant_df = pd.read_csv('part_one\\data\\restaurant_info.csv')
unique_pricerange = set(restaurant_df['pricerange'].dropna().str.lower())
unique_areas = set(restaurant_df['area'].dropna().str.lower())
unique_foodtype = set(restaurant_df['food'].dropna().str.lower())

# 1. Add new properties into the CSV file
df = pd.read_csv('part_one/data/restaurant_info.csv')

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

# 2. Add question in dialog manager

user_input = "I want moderately priced british food in the west part of town."
print(user_input)

preferences_dict = extract_preferences(user_input, unique_areas, unique_foodtype, unique_pricerange)
print(preferences_dict)

possible_restaurants = lookup(restaurant_df, preferences_dict)
possible_restaurants["consequent"] = None
print(possible_restaurants)

user_input = input("Do you have any additional requirements? ")
user_input = re.sub(r'[^\w\s]', '', user_input)
words = set(user_input.split())

# 3. Extract additional requirements
additional_requirements = []
additional_req_signal = {"touristic", "assigned seats", "children", "romantic"}
additional_requirements.append(words & additional_req_signal)


# 4. Apply inference rules to update possible_restaurants list
for restaurant in possible_restaurants:

    # Find all the values from the df
    restaurant_info = df[df["restaurantname"] == restaurant]
    restaurant["consequent"] = apply_inference_rules(restaurant_info, additional_requirements)

    
# ------------------------------------------------------------------------------

def apply_inference_rules(restaurant_info, additional_requirements):
    """
    Input: restaurant info row from csv file & additional requirements (list)
    Output: consequent
    """
    
    # Extract restaurant info
    name = restaurant_info["restaurantname"]
    pricerange = restaurant_info["pricerange"]
    food = restaurant_info["food"]
    food_quality = restaurant_info["food_quality"]
    crowdedness = restaurant_info["crowdedness"]
    length_of_stay = restaurant_info["length_of_stay"]

    #initializing consequent
    consequent = None

    #setting amount of requirements
    num_requirements = additional_requirements.count

    #loop over all requirements
    for i in range(num_requirement):
        if additional_requirements[i] == 'touristic':
            if (princerange == 'cheap' and food_quality == 'good'):
                consequent.append('touristic')



    

    return consequent


# ------------------------------------------------------------------------------
# 4. Answer and explain

