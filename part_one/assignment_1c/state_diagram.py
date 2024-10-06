from functions import *
import pandas as pd

class State_diagram:
    def __init__(self):
        self.state = "welcome"
        self.is_state = True
        self.preferences_dict = {"area": None,
                                 "food type": None,
                                 "pricerange": None}
                        
        self.lievenshtein_distance_threshold = 3
        self.allow_dialog_restart = 'y'

        self.restaurant_df = pd.read_csv('part_one\\data\\restaurant_info.csv')
        self.restaurant_df = add_reasoning_data(self.restaurant_df)

        self.unique_pricerange = set(self.restaurant_df['pricerange'].dropna().str.lower())
        self.unique_areas = set(self.restaurant_df['area'].dropna().str.lower())
        self.unique_foodtype = set(self.restaurant_df['food'].dropna().str.lower())

        self.available_restaurants = None
        self.dialog_act = None

        self.formal_dialogue = [
            "System: You are welcome. Have a nice day!", 
            "System: I am sorry, I did not understand that. Please provide me with more information.",
            "System: I am sorry, there are no restaurants with those preferences. Please provide me with different preferences.",
            "System: I have all the information I need. I will now suggest a restaurant.",
            "System: In what area would you like to eat?",
            "System: What type of food are you looking for?",
            "System: What type of price range are you looking for?",
            "System: I am sorry, I did not understand that. Please provide me with more information about your preferences.",
            "System: What more information would you like to know?",
            "System: I'm sorry, there are no more restaurants to suggest.",
            "System: I'm sorry, I didn't understand your request.",
            "System: Hello, welcome to the Cambridge restaurant system? You can ask for restaurants by area, price range or food type. How may I help you?",
            "System: Please enter your preferences from the following options:\n"
            "Type 'touristic' if you want a touristic restaurant,\n"
            "Type 'assigned seats' if you want the restaurant to have assigned seating,\n"
            "Type 'children' if you want the restaurant to be suitable for children,\n"
            "Type 'romantic' if you want a romantic restaurant.\n"
            "Type 'no additional requirements' if you have no additional requirements."
        ]
        
        self.informal_dialogue = [
            "System: Alright, take it easy. See you next time!",  
            "System: Uh... I didn't quite catch that... Mind telling me again?",
            "System: Hey, it doesn't look like there's any places that fit what you want. Maybe switch up your demands a bit and check again...",
            "System: Alright, got it all down. Let's see if you'll like this one...",
            "System: Where in town do ya wanna eat?",
            "System: What do you feel like eating?",
            "System: Alright, so how much do you wanna pay for this?",
            "System: Uhm, this is a little embarrassing... but can you, like, make that clearer?",
            "System: Alright, alright, what more do you wanna know?",
            "System: Sorry, friend, I've got no other places I can suggest...",
            "System: Sorry, but, like, I don't get what you want me to tell you...",
            "System: Hey there! Welcome to the Cambridge restaurant system! You can ask for restaurants by area, price range or food type. How can I help you out?",
            "System: Please enter your preferences from the following options:\n"
            "Type 'touristic' if you want a touristic restaurant,\n"
            "Type 'assigned seats' if you want the restaurant to have assigned seating,\n"
            "Type 'children' if you want the restaurant to be suitable for children,\n"
            "Type 'romantic' if you want a romantic restaurant.\n"
            "Type 'no additional requirements' if you have no additional requirements."
        ]
        
        self.system_utterances = self.formal_dialogue
    
    def ask_preferences(self, user_input):
        new_preferences = extract_preferences(user_input, self.unique_areas, self.unique_foodtype, self.unique_pricerange)

        # Update the existing preferences_dict
        for key, value in new_preferences.items():
            if value is not None:
                self.preferences_dict[key] = value

        missing_preferences = [pref for pref, value in self.preferences_dict.items() if value is None]

        self.available_restaurants = lookup(self.restaurant_df, self.preferences_dict)
        if self.available_restaurants.empty:
            print(f"System: I am sorry, there are no restaurants with those preferences: "
                  f"Area: {self.preferences_dict['area']}, "
                  f"Food Type: {self.preferences_dict['food type']}, "
                  f"Price Range: {self.preferences_dict['pricerange']}. "
                  "Please provide me with different preferences.")
            self.state = "preference_doesnt_exist"
        elif not missing_preferences:
            print(self.system_utterances[12])
            self.state = "additional_requirements"
        elif "area" in missing_preferences:
            print(self.system_utterances[4])
            self.state = "ask_area"
        elif "food type" in missing_preferences:
            print(self.system_utterances[5])
            self.state = "ask_food_type"
        elif "pricerange" in missing_preferences:
            print(self.system_utterances[6])
            self.state = "ask_price_range"

        self.is_state = True

    def state_transition_function(self, user_input=None, levenshtein_distance_threshold=3):
        if self.dialog_act == "thankyou" or self.dialog_act == "bye":
            print(self.system_utterances[0])
            self.state = "endstate"
        
        elif "restart" in user_input and self.allow_dialog_restart == 'y':
            self.state = "welcome"
            self.preferences_dict = {"area": None, "food type": None, "pricerange": None}
            self.available_restaurants = None
            self.dialog_act = None
            print(self.system_utterances[11])
            
        elif self.state == "welcome":
            if self.dialog_act == "inform" or self.dialog_act == "null":
                self.ask_preferences(user_input)
            else:
                print(self.system_utterances[11])

        elif self.state == "ask_area":
            if self.dialog_act == "inform":
                self.ask_preferences(user_input)
            else:
                print(self.system_utterances[7])

        elif self.state == "ask_food_type":
            if self.dialog_act == "inform":
                self.ask_preferences(user_input)
            else:
                print(self.system_utterances[7])

        elif self.state == "ask_price_range":
            if self.dialog_act == "inform":
                self.ask_preferences(user_input)
            else:
                print(self.system_utterances[7])

        elif self.state == "preference_doesnt_exist":
            if self.dialog_act == "inform" or self.dialog_act == "reqalts":
                self.ask_preferences(user_input)
        
        elif self.state == "additional_requirements":
            if "no additional requirements" in user_input:
                print(self.system_utterances[3])
                suggest_restaurant(self.available_restaurants)
                self.state = "suggest_restaurant"
            else:
                valid_restaurants = apply_inference_rules(self.available_restaurants, user_input)
                print(valid_restaurants.head())

                if not valid_restaurants.empty:
                    self.available_restaurants = valid_restaurants
                    print(self.system_utterances[3])
                    suggest_restaurant(self.available_restaurants)
                    self.state = "suggest_restaurant"
                else:
                    print(self.system_utterances[2])
                    self.state = "additional_requirements"

        elif self.state == "suggest_restaurant":
            if self.dialog_act == "request":
                self.state = "give_info"
                self.is_state = False
            
            elif self.dialog_act == "inform":
                self.ask_preferences(user_input)
            
            elif self.dialog_act == "reqalts":
                if len(self.available_restaurants) > 1:
                    self.available_restaurants = self.available_restaurants.iloc[1:].reset_index(drop=True)
                    suggest_restaurant(self.available_restaurants)
                else:
                    print(self.system_utterances[9])
                    self.state = "ask_preferences"
                    self.is_state = False    
            else:
                print(self.system_utterances[10])
                self.state = "suggest_restaurant"
                
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
                    print(self.system_utterances[10])
                
                self.state = "suggest_restaurant"

            elif self.dialog_act == "inform":
                print(self.system_utterances[8])
            
            self.is_state = True

    def run(self, model, vectorizer, vectorized, levenshtein_distance_threshold=3, allow_dialog_restart='y', formal=True):        
        self.lievenshtein_distance_threshold = levenshtein_distance_threshold

        if allow_dialog_restart == 'y':
            self.allow_dialog_restart = 'y'

        if not formal:
            self.system_utterances = self.informal_dialogue

        print(self.system_utterances[11])

        while self.state != "endstate":
            if self.is_state:
                user_input = input("You: ").lower()

                vectorized_user_input = vectorizer.transform([user_input])

                # Classifying user input using ML model
                if vectorized:
                    self.dialog_act = model.predict(vectorized_user_input)[0]
                else:
                    self.dialog_act = model.predict([[user_input]])[0]
                self.state_transition_function(user_input)

            else:
                self.state_transition_function(user_input=user_input)