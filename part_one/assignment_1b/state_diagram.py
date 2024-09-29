from state import State
from functions import *


class State_diagram:
    def __init__(self):
        self.state = "welcome"
        self.area = None
        self.food_type = None
        self.price_range = None
        self.is_state = True
        self.restaurant = None
        self.other_options = None
        self.preferences_dict = {"area": None,
                        "food type": None,
                        "pricerange": None}
                        
        self.restaurant_df = pd.read_csv('part_one\\data\\restaurant_info.csv')
        self.unique_pricerange = set(self.restaurant_df['pricerange'].dropna().str.lower())
        self.unique_areas = set(self.restaurant_df['area'].dropna().str.lower())
        self.unique_foodtype = set(self.restaurant_df['food'].dropna().str.lower())
        

    def preferences_incorrect(self):
        unique_sets = {
            "pricerange": self.unique_pricerange,
            "area": self.unique_areas,
            "food type": self.unique_foodtype
        }

        for key, value in self.preferences_dict.items():
            if key in unique_sets and value not in unique_sets[key]:
                if key != None:
                    return key
        return False


    def state_transition_function(self, user_input = None, dialog_act = None):
        if self.state == "welcome":
            if dialog_act == "inform" or dialog_act == "null":
                self.state = "ask_preferences"
                self.is_state = False
            else:
                print("System: I am sorry, I did not understand that. Please provide me with more information.")


        elif self.state == "ask_preferences":
            self.preferences_dict = extract_preferences(user_input, self.unique_areas, self.unique_foodtype, self.unique_pricerange)
            # self.preferences_dict = self.preferences_dict = {"area": None,
            #             "food type": "chinese",
            #             "pricerange": None}
            
            missing_preferences = [pref for pref, value in self.preferences_dict.items() if value is None]

            # prefences_exists = self.preferences_incorrect()
            prefences_exists = False

            if prefences_exists:
                print(f"System: I am sorry, {prefences_exists} is not a valid preference. Please provide me with a valid preference.")
                self.state = "preference_doesnt_exist"
            elif not missing_preferences:
                print("System: I have all the information I need. I will now suggest a restaurant.")
                self.state = "suggest_restaurant"
            elif "area" in missing_preferences:
                print("System: In what area would you like to eat?")
                self.state = "ask_area"
            elif "food_type" in missing_preferences:
                print("System: What type of food are you looking for?")	
                self.state = "ask_food_type"
            elif "price_range" in missing_preferences:
                print("System: What type of price range are you looking for?")
                self.state = "ask_price_range"
            else:
                print('ya donkey')
            print('hi')
            self.is_state = True


        elif self.state == "ask_area":
            if dialog_act == "inform":
                print('----------------------------------------')
                extracted_preferences = extract_preferences(user_input, self.unique_areas, self.unique_foodtype, self.unique_pricerange)
                self.preferences_dict["area"] = extracted_preferences.get("area", None)
                self.state = "ask_preferences"
                print(extracted_preferences)
                print(self.preferences_dict)
                print(self.state)

                self.is_state = False
            else:
                print("System: I am sorry, I did not understand that. Please provide me with more information about your preferences.")


        elif self.state == "ask_food_type":
            if dialog_act == "inform":
                extracted_preferences = extract_preferences(user_input, self.unique_areas, self.unique_foodtype, self.unique_pricerange)
                self.preferences_dict["food type"] = extracted_preferences.get("food type", None)
                self.state = "ask_preferences"
                self.is_state = False
            else:
                print("System: I am sorry, I did not understand that. Please provide me with more information.")
        

        elif self.state == "ask_price_range":
            if dialog_act == "inform":
                extracted_preferences = extract_preferences(user_input, self.unique_areas, self.unique_foodtype, self.unique_pricerange)
                self.preferences_dict["pricerange"] = extracted_preferences.get("pricerange", None)
                self.state = "ask_preferences"
                self.is_state = False
            else:
                print("System: I am sorry, I did not understand that. Please provide me with more information.")
        

        elif self.state == "preference_doesnt_exist":
            print(f"System: I am sorry, {prefences_exists} is not a valid preference. Please provide me with a valid preference.")
            self.state = "ask_preferences"
            self.is_state = False
        
        elif self.state == "suggest_restaurant":
            print("System: I will now suggest a restaurant.")
            self.state = "endstate"
        
        else:
            print('big mistake')
            print(self.state)
            print(self.dialog_act)


    def run(self, model, vectorizer):        
        print("System: Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?")
        # Save all the options for typefood, area and location
        
        user_input = None
        
        while self.state != "endstate":
            if self.is_state:
                user_input = input("You: ").lower()
                vectorized_user_input = vectorizer.transform([user_input])

                #classifying user input using ML model
                dialog_act = model.predict(vectorized_user_input)
                print(self.state, dialog_act)
                self.state_transition_function(user_input, dialog_act)

            else:
                self.state_transition_function(user_input=user_input)



    #   elif self.state == "ask_food":
    #         self.food_type = user_input
    #         self.state = "ask_price"
    #         print("System: What type of price range are you looking for?")

    #     elif self.state == "ask_price":
    #         self.price_range = user_input
    #         self.state = "double_check"
    #         print(f"System: So you want to eat at {self.area} place?")

    #     elif self.state == "double_check":
    #         if user_input == "yes":
    #             self.state = "suggest_restaurant"
    #             print(f"System: {self.restaurant} is a nice restaurant to eat at")
    #         else:
    #             self.state = "no_match"
    #             print("System: Sorry, such a restaurant does not exist")

    #     elif self.state == "suggest_restaurant":
    #         self.state = "give_info"
    #         print(f"System: The info for this restaurant is {self.other_options}")

    #     elif self.state == "give_info":
    #         self.state = "endstate"
    #         print("System: The conversation has ended.")

    #     elif self.state == "no_match":
    #         self.state = "endstate"
    #         print("System: The conversation has ended.")

    #     else:
    #         self.state = "endstate"
    #         print("System: The conversation has ended.")