from utils import lookup, suggest_restaurant, add_reasoning_data
from preference_extraction import extract_preferences
from inference_rules import apply_inference_rules
import pandas as pd
import time


class State_diagram:
    def __init__(self):
        self.state = "welcome"
        self.is_state = True
        self.preferences_dict = {"area": None,
                                 "food type": None,
                                 "pricerange": None}
                        
        self.lievenshtein_distance_threshold = 3

        self.restaurant_df = pd.read_csv('part_one\\data\\restaurant_info.csv')
        self.restaurant_df = add_reasoning_data(self.restaurant_df)

        self.unique_pricerange = set(self.restaurant_df['pricerange'].dropna().str.lower())
        self.unique_areas = set(self.restaurant_df['area'].dropna().str.lower())
        self.unique_foodtype = set(self.restaurant_df['food'].dropna().str.lower())
              
        self.allow_dialog_restart = 'n'
        self.available_restaurants = None
        self.dialog_act = None

        self.additional_requirements_done = False
        self.suggested_restaurant_index = None

        self.formal_dialogue = [
            "System: You are welcome. Please have a pleasant day.",
            "System: I apologize, I did not fully understand your request. Could you kindly provide additional information?",
            "System: I regret to inform you that there are no restaurants available with those preferences. May I kindly ask for different preferences?",
            "System: In which area would you prefer to dine?",
            "System: What type of cuisine are you seeking?",
            "System: What price range are you comfortable with?",
            "System: I apologize, but I did not understand your request. Could you please clarify your preferences?",
            "System: What additional information would you like to receive?",
            "System: My apologies, but there are no further restaurant suggestions available.",
            "System: I'm sorry, but I did not quite understand your request.",
            "System: Greetings, and welcome to the Cambridge Restaurant System. You may ask for restaurant suggestions by area, price range, or type of cuisine. How may I assist you today?",
            "System: Kindly enter your preferences from the following options. Please note that selecting preferences that contradict each other (e.g., a restaurant cannot be both romantic and not romantic) may result in no suitable recommendations:\n"
            "Type 'touristic' for a touristic restaurant,\n"
            "Type 'assigned seats' for assigned seating,\n"
            "Type 'children' for a child-friendly restaurant,\n"
            "Type 'romantic' for a romantic restaurant,\n"
            "Type 'no additional requirements' if you have no specific preferences.",
            "System: I regret to inform you that there are no restaurants matching those preferences."
        ]

        self.informal_dialogue = [
            "System: You got it! Take care and see you next time!",
            "System: Whoops, I didn’t catch that... Can you say it again?",
            "System: Hmm, looks like there aren’t any places that match what you're after. Maybe tweak your preferences and give it another go?",
            "System: So, where do you wanna eat in town?",
            "System: What kind of food are you in the mood for?",
            "System: How much are you looking to spend on this meal?",
            "System: Hmm, that didn’t come through clearly. Could you say it a bit differently?",
            "System: Alright, what else do you wanna know?",
            "System: Uh-oh, I’m all out of restaurant suggestions for you.",
            "System: Uh, I didn’t quite get that. What exactly are you asking for?",
            "System: Hey! Welcome to the Cambridge Restaurant System! You can ask about restaurants by area, price range, or food type. What can I do for ya?",
            "System: Drop your preferences from the list below. Heads up: if you pick things that don’t really go together (like a place can’t be both romantic and not romantic), it might be tricky to find anything:\n"
            "Type 'touristic' for a touristy spot,\n"
            "Type 'assigned seats' for places with assigned seating,\n"
            "Type 'children' for kid-friendly spots,\n"
            "Type 'romantic' if you're looking for romance,\n"
            "Type 'no additional requirements' if you don’t care much.",
            "System: Hmm, sorry, but I couldn’t find any restaurants that match those preferences."
        ]

        
        self.system_utterances = self.formal_dialogue
    

    def ask_preferences(self, user_input):
        """
        Function to ask the user for preferences and update the state accordingly
        """
        new_preferences = extract_preferences(user_input, self.unique_areas, self.unique_foodtype, self.unique_pricerange)

        # Update the existing preferences_dict
        for key, value in new_preferences.items():
            if value is not None:
                self.preferences_dict[key] = value

        missing_preferences = [pref for pref, value in self.preferences_dict.items() if value is None]

        self.available_restaurants = lookup(self.restaurant_df, self.preferences_dict)
        if self.available_restaurants.empty:
            print(self.system_utterances[12])
            print(f"Area: {self.preferences_dict['area']}, "
                  f"Food Type: {self.preferences_dict['food type']}, "
                  f"Price Range: {self.preferences_dict['pricerange']}. "
                  "Please provide me with different preferences.")
            self.state = "preference_doesnt_exist"
        elif not missing_preferences:
            if not self.additional_requirements_done:
                print(self.system_utterances[11])
                self.state = "additional_requirements"
            else:
                self.suggested_restaurant_index = suggest_restaurant(self.available_restaurants)
                self.state = "suggest_restaurant"
        elif "area" in missing_preferences:
            print(self.system_utterances[3])
            self.state = "ask_area"
        elif "food type" in missing_preferences:
            print(self.system_utterances[4])
            self.state = "ask_food_type"
        elif "pricerange" in missing_preferences:
            print(self.system_utterances[5])
            self.state = "ask_price_range"

        self.is_state = True


    def state_transition_function(self, user_input=None):
        """
        Function to transition between states based on the user input
        """
        if self.dialog_act == "thankyou" or self.dialog_act == "bye":
            print(self.system_utterances[0])
            self.state = "endstate"
        
        elif "restart" in user_input and self.allow_dialog_restart == 'y':
            self.state = "welcome"
            self.preferences_dict = {"area": None, "food type": None, "pricerange": None}
            self.available_restaurants = None
            self.dialog_act = None
            print(self.system_utterances[10])
            
        elif self.state == "welcome":
            if self.dialog_act == "inform" or self.dialog_act == "null" or self.dialog_act == "hello":
                self.ask_preferences(user_input)
            else:
                print(self.system_utterances[10])

        elif self.state == "ask_area":
            if self.dialog_act == "inform":
                self.ask_preferences(user_input)
            else:
                print(self.system_utterances[6])

        elif self.state == "ask_food_type":
            if self.dialog_act == "inform":
                self.ask_preferences(user_input)
            else:
                print(self.system_utterances[6])

        elif self.state == "ask_price_range":
            if self.dialog_act == "inform":
                self.ask_preferences(user_input)
            else:
                print(self.system_utterances[6])

        elif self.state == "preference_doesnt_exist":
            if self.dialog_act == "inform" or self.dialog_act == "reqalts":
                self.ask_preferences(user_input)
        
        elif self.state == "additional_requirements":
            if "no additional requirements" in user_input:
                self.suggested_restaurant_index = suggest_restaurant(self.available_restaurants)
                self.state = "suggest_restaurant"
                self.additional_requirements_done = True
            else:
                valid_restaurants, requirements = apply_inference_rules(self.available_restaurants, user_input)

                if not valid_restaurants.empty:
                    requirements_str = ', '.join(requirements)
                    print(f'System: The restaurants have been filtered by the requirements: {requirements_str}')
                    self.available_restaurants = valid_restaurants
                    self.suggested_restaurant_index = suggest_restaurant(self.available_restaurants)
                    self.state = "suggest_restaurant"
                    self.additional_requirements_done = True
                else:
                    print(self.system_utterances[2])
                    self.state = "additional_requirements"

        elif self.state == "suggest_restaurant":
            if self.dialog_act == "request":
                self.state = "give_information"
                self.is_state = False
            
            elif self.dialog_act == "inform":
                self.ask_preferences(user_input)
            
            elif self.dialog_act == "reqalts":
                if len(self.available_restaurants) > 1:
                    self.available_restaurants = self.available_restaurants.drop(self.suggested_restaurant_index).reset_index(drop=True)

                    self.suggested_restaurant_index = suggest_restaurant(self.available_restaurants)
                    self.state = "suggest_restaurant"
                else:
                    print(self.system_utterances[8])
                    self.ask_preferences(user_input)
            else:
                print(self.system_utterances[9])
                self.state = "suggest_restaurant"
                
        elif self.state == "give_information":
            if self.dialog_act == "request":
                restaurant_info = self.available_restaurants.iloc[self.suggested_restaurant_index]
                
                if "phone" in user_input:
                    print(f"System: The phone number for this restaurant is {restaurant_info['phone']}")
                elif "address" in user_input:
                    print(f"System: The address for this restaurant is {restaurant_info['addr']}")
                    print(self.system_utterances[0])
                    self.state = "endstate"
                    return None
                elif "postcode" in user_input:
                    print(f"System: The postcode for this restaurant is {restaurant_info['postcode']}")
                else:
                    print(self.system_utterances[9])
                
                self.state = "suggest_restaurant"

            elif self.dialog_act == "inform":
                print(self.system_utterances[7])
                self.state = "give_information"
            else:
                print(self.system_utterances[9])
                self.state = "suggest_restaurant"
            
            self.is_state = True


    def run(self, model, vectorizer, vectorized, levenshtein_distance_threshold=3, allow_dialog_restart='y', formal=True):    
        """
        Function to run the state diagram.
        """    
        self.lievenshtein_distance_threshold = levenshtein_distance_threshold

        self.allow_dialog_restart = allow_dialog_restart

        if self.allow_dialog_restart == 'y':
            self.allow_dialog_restart = 'y'

        if not formal:
            self.system_utterances = self.informal_dialogue

        print("Hi, thank you for agreeing to help us with our research. We are interested in understanding how people interact with chatbots.")
        print("Your task is to find the address of a restaurant in Cambridge where you'd like to eat, using our chatbot. The conversation will end when the address is found.\n")

        print('Extra information:')
        print("Available areas to choose from: 'centre', 'north', 'south', 'east', 'west'.")
        print("Available prices to choose from: 'cheap', 'moderate', 'expensive'.")
        print("Say 'bye' to end the converstation anytime or 'restart' to start over.\n")

        input("Press Enter to start the conversation.\n")


        print(self.system_utterances[10])

        # Initialize runtime and state turn counter
        start_time = time.time()
        state_turns = 0

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

                # Increment state turn counter
                state_turns += 1

            else:
                self.state_transition_function(user_input=user_input)

        # Calculate runtime
        end_time = time.time()
        runtime = end_time - start_time

        # Print findings
        print(f"Runtime: {runtime:.2f} seconds")
        print(f"Number of state turns: {state_turns}")
