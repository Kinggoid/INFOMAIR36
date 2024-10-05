import pandas as pd
import numpy as np
import random
from main_1b_copy import extract_preferences, lookup
import re

# 1. Add new properties into the CSV file
df = pd.read_csv('part_one\\restaurant_info.csv')

food_quality_options = ["good", "not good"]
crowdedness_options = ["busy", "calm"]
length_of_stay_options = ["long", "short"]

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

preferences_dict = extract_preferences(user_input)
print(preferences_dict)

possible_restaurants = lookup(preferences_dict)
print(possible_restaurants)

user_input = input("Do you have any additional requirements? ")
user_input = re.sub(r'[^\w\s]', '', user_input)
words = set(user_input.split())

# 3. Extract additional requirements
additional_reqs = []
additional_req_signal = {"touristic", "assigned seats", "children", "romantic"}
negate = {"no", "not"}
consequent = words & additional_req_signal

if words & negate:
    boolean = False
else:
    boolean = True

# 4. Apply inference rules to update possible_restaurants list
for restaurant in possible_restaurants:

    # Find all the values from the df
    restaurant_info = df[df["restaurantname"] == restaurant]

    # 
    antesedant = apply_inference_rules(restaurant_info, boolean)
    
# ------------------------------------------------------------------------------

def apply_inference_rules(restaurant_info, additional_requirement, boolean):
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

    # Inference rules
    if additional_requirement == "touristic" and boolean == True:

        # Inference rules 1 and 2:
        if (pricerange == "cheap" and food_quality == "good") or food != "romanian":
            consequent = "touristic"
        else:
            consequent = ""


# ------------------------------------------------------------------------------

# 4. Answer and explain

