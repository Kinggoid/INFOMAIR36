import random

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