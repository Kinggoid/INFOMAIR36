import pandas as pd
import numpy as np
import random
from functions import extract_preferences, lookup
import re


restaurant_df = pd.read_csv('part_one\\data\\restaurant_info.csv')
unique_pricerange = set(restaurant_df['pricerange'].dropna().str.lower())
unique_areas = set(restaurant_df['area'].dropna().str.lower())
unique_foodtype = set(restaurant_df['food'].dropna().str.lower())

#to better understand my dataframes
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

# 1. Add new properties into the CSV file
df = pd.read_csv('part_one/data/restaurant_info.csv')

food_quality_options = ["good", "not good"]
crowdedness_options = ["busy", "not busy"]
length_of_stay_options = ["long stay", "short stay"]

food_quality_list = []
crowdedness_list = []
length_of_stay_list = []

#random seed to ensure the same outcomes for easier testing
random.seed(69420)

#giving random values for food quality, crowdedness and length of stay
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

possible_restaurants = lookup(df, preferences_dict)
possible_restaurants["consequent"] = None
print(possible_restaurants)

user_input = input("Do you have any additional requirements? ")
user_input = re.sub(r'[^\w\s]', '', user_input)
words = set(user_input.split())

# 3. Extract additional requirements
additional_req_signal = {"touristic", "assigned seats", "children", "romantic"}

# Use list comprehension to filter the matching requirements
additional_requirements = [match for match in additional_req_signal if match in words]

# Prevent contradictory request by specifying a priority
#if var in possible_restaurants == 'romanian' and var2 in additional_requirements == 'touristic':
#    decision = input('SYSTEM: Conflicting requirements. Food cannot be romanian and touristic. Would you rather find food that is romanian or touristic?')
    # Update the additional_requirements or something using this information. Do something with this info 

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

    # initializing consequent
    consequent = []

    # setting amount of requirements
    num_requirements = len(additional_requirements)
    

    # loop over all requirements
    for i in range(num_requirements):
        #rule 1
        if additional_requirements[i] == 'touristic':
            if pricerange == 'cheap' and food_quality == 'good':
                consequent.append('touristic')
        #rule 3
        if additional_requirements[i] == 'assigned seats':
            if length_of_stay == 'long stay':
                consequent.append('assigned seats')
        #rule 6 
        if additional_requirements[i] == 'romantic':
            if length_of_stay == 'long stay':
                consequent.append('romantic')

    
    return consequent if consequent else []

# 4. Apply inference rules to update possible_restaurants list
for index, restaurant in possible_restaurants.iterrows():
    # Find all the values from the df
    restaurant_info = df[df['restaurantname'] == restaurant['restaurantname']]
    if not restaurant_info.empty:
        # Apply inference rules to get the new consequent for this restaurant
        consequent = apply_inference_rules(restaurant_info.iloc[0], additional_requirements)
        
        # Update the 'consequent' column for this restaurant in the dataframe
        possible_restaurants.at[index, 'consequent'] = consequent
        print(possible_restaurants)

# 5. Now filter restaurants based on requirements and the restaurant consequent property
