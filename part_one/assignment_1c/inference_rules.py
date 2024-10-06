import re
import pandas as pd

def apply_inference_rules(restaurant_df, user_input):
    """
    output: restaurant_df with all restaurants that fit the additional_requirements
    """
    # Ensure user input is a string, convert to lowercase, remove non-alphanumeric characters, and split into words
    words = set(re.sub(r'[^\w\s]', '', str(user_input).lower()).split())

    # Define the additional requirements
    additional_req_signal = {"touristic", "assigned seats", "children", "romantic"}

    # Check for "assigned seats" as a single requirement
    if "assigned" in words and "seats" in words:
        words.add("assigned seats")

    # Filter the matching requirements
    additional_requirements = [match for match in additional_req_signal if match in words]

    # Initialize an empty DataFrame to store the valid rows
    valid_restaurants_df = pd.DataFrame(columns=restaurant_df.columns)

    for _, row in restaurant_df.iterrows():
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
            if crowdedness != "busy" and stay_duration == "long stay":  # It is a romantic restaurant	
                pass  
            else:
                continue

        # If the row meets all requirements, add it to the new DataFrame
        valid_restaurants_df = pd.concat([valid_restaurants_df, pd.DataFrame([row])], ignore_index=True)

    # Reset the index of the new DataFrame
    valid_restaurants_df.reset_index(drop=True, inplace=True)
    return valid_restaurants_df, additional_requirements