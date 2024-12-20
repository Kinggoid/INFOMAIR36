from functions import *
import pandas as pd

class State_diagram:
    def __init__(self):
        self.state = "welcome"
        self.is_state = True
        self.preferences_dict = {"area": None,
                                 "food type": None,
                                 "pricerange": None}

        self.restaurant_df = pd.read_csv('part_one\\data\\restaurant_info.csv')
        self.unique_pricerange = set(self.restaurant_df['pricerange'].dropna().str.lower())
        self.unique_areas = set(self.restaurant_df['area'].dropna().str.lower())
        self.unique_foodtype = set(self.restaurant_df['food'].dropna().str.lower())

        self.available_restaurants = None
        self.dialog_act = None

    def state_transition_function(self, user_input=None):
        if self.dialog_act == "thankyou" or self.dialog_act == "bye":
            print("System: You are welcome. Have a nice day!")
            self.state = "endstate"

        elif self.state == "welcome":
            if self.dialog_act == "inform" or self.dialog_act == "null":
                self.state, self.available_restaurants = ask_preferences(
                    user_input, self.preferences_dict, self.unique_areas, self.unique_foodtype, self.unique_pricerange, self.restaurant_df)
            else:
                print("System: I am sorry, I did not understand that. Please provide me with more information.")

        elif self.state == "ask_preferences":
            # Extract new preferences
            new_preferences = extract_preferences(user_input, self.unique_areas, self.unique_foodtype, self.unique_pricerange)

            # Update the existing preferences_dict
            for key, value in new_preferences.items():
                if value is not None:
                    self.preferences_dict[key] = value

            missing_preferences = [pref for pref, value in self.preferences_dict.items() if value is None]

            self.available_restaurants = lookup(self.restaurant_df, self.preferences_dict)
            if self.available_restaurants.empty:
                print("System: I am sorry, there are no restaurants with those preferences. Please provide me with different preferences.")
                self.state = "preference_doesnt_exist"
            elif not missing_preferences:
                print("System: I have all the information I need. I will now suggest a restaurant.")

                # Suggest the first restaurant from the filtered DataFrame
                suggested_restaurant = self.available_restaurants.iloc[0]

                # Extract details of the suggested restaurant
                restaurant_name = suggested_restaurant['restaurantname']
                restaurant_food = suggested_restaurant['food']
                restaurant_area = suggested_restaurant['area']
                restaurant_pricerange = suggested_restaurant['pricerange']

                # Print the suggestion
                print(f"System: I suggest {restaurant_name}. It serves {restaurant_food} food in the {restaurant_area} area and falls within the {restaurant_pricerange} price range.")
                self.state = "suggest_restaurant"
            elif "area" in missing_preferences:
                print("System: In what area would you like to eat?")
                self.state = "ask_area"
            elif "food type" in missing_preferences:
                print("System: What type of food are you looking for?")
                self.state = "ask_food_type"
            elif "pricerange" in missing_preferences:
                print("System: What type of price range are you looking for?")
                self.state = "ask_price_range"
            else:
                print('For testing. If you read this, something went wrong')
            self.is_state = True

        elif self.state == "ask_area":
            if self.dialog_act == "inform":
                extracted_preferences = extract_preferences(user_input, self.unique_areas, self.unique_foodtype, self.unique_pricerange)
                self.preferences_dict["area"] = extracted_preferences.get("area", None)
                self.state, self.available_restaurants = ask_preferences(
                    user_input, self.preferences_dict, self.unique_areas, self.unique_foodtype, self.unique_pricerange, self.restaurant_df)
            else:
                print("System: I am sorry, I did not understand that. Please provide me with more information about your preferences.")

        elif self.state == "ask_food_type":
            if self.dialog_act == "inform":
                extracted_preferences = extract_preferences(user_input, self.unique_areas, self.unique_foodtype, self.unique_pricerange)
                self.preferences_dict["food type"] = extracted_preferences.get("food type", None)
                self.state, self.available_restaurants = ask_preferences(
                    user_input, self.preferences_dict, self.unique_areas, self.unique_foodtype, self.unique_pricerange, self.restaurant_df)
            else:
                print("System: I am sorry, I did not understand that. Please provide me with more information about your preferences.")

        elif self.state == "ask_price_range":
            if self.dialog_act == "inform":
                extracted_preferences = extract_preferences(user_input, self.unique_areas, self.unique_foodtype, self.unique_pricerange)
                self.preferences_dict["pricerange"] = extracted_preferences.get("pricerange", None)
                self.state, self.available_restaurants = ask_preferences(
                    user_input, self.preferences_dict, self.unique_areas, self.unique_foodtype, self.unique_pricerange, self.restaurant_df)
            else:
                print("System: I am sorry, I did not understand that. Please provide me with more information about your preferences.")

        elif self.state == "preference_doesnt_exist":
            if self.dialog_act == "inform" or self.dialog_act == "reqalts":
                self.state, self.available_restaurants = ask_preferences(
                    user_input, self.preferences_dict, self.unique_areas, self.unique_foodtype, self.unique_pricerange, self.restaurant_df)

        elif self.state == "suggest_restaurant":
            if self.dialog_act == "request":
                self.state = "give_info"
                self.is_state = False

            elif self.dialog_act == "inform":
                print("System: What more information would you like to know?")
                self.state = "ask_preferences"
                self.is_state = False

            elif self.dialog_act == "reqalts":
                if len(self.available_restaurants) > 1:
                    self.available_restaurants = self.available_restaurants.iloc[1:].reset_index(drop=True)
                    suggest_restaurant(self.available_restaurants)
                else:
                    print("System: I'm sorry, there are no more restaurants to suggest.")
                self.state = "ask_preferences"
                self.is_state = False

        elif self.state == "give_info":
            if self.dialog_act == "request":
                restaurant_info = self.available_restaurants.iloc[0]

                if "phone" in user_input:
                    print(f"System: The phone number for this restaurant is {restaurant_info['phone']}")
                elif "address" in user_input:
                    print(f"System: The address for this restaurant is {restaurant_info['addr']}")
                elif "postcode" in user_input:
                    print(f"System: The postcode for this restaurant is {restaurant_info['postcode']}")
                else:
                    print("System: I'm sorry, I didn't understand your request.")

                self.state = "suggest_restaurant"

            elif self.dialog_act == "inform":
                print("System: What more information would you like to know?")

            self.is_state = True

    def run(self, model, vectorizer):
        """
        This function runs the state diagram of the system. It takes in the ML model and the vectorizer as inputs.
        """
        print("System: Hello, welcome to the Cambridge restaurant system? You can ask for restaurants by area, price range or food type. How may I help you?")

        user_input = None

        while self.state != "endstate":
            if self.is_state:
                user_input = input("You: ").lower()

                vectorized_user_input = vectorizer.transform([user_input])

                # Classifying user input using ML model
                self.dialog_act = model.predict(vectorized_user_input)[0]
                self.state_transition_function(user_input)

            else:
                self.state_transition_function(user_input=user_input)