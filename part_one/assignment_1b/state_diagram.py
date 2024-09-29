from state import State
from functions import *


class State_diagram:
    def __init__(self):
        self.state = "welcome"
        self.area = None
        self.food_type = None
        self.price_range = None
        self.response = True
        self.restaurant = None
        self.other_options = None

    
    def add_state(self, state):
        self.states.append(state)
    
    def get_state(self, state_name):
        for state in self.states:
            if state.name == state_name:
                return state
        return None
    
    def get_next_state(self, current_state, input):
        return self.get_state(current_state).next_state(input)
    
    # Example dialog simulation -------------------------------------------------------------
    def state_transition_function(initial_state, user_input, dialog_act):
        #show current state
        current_state = initial_state
        print(f"Current state: {current_state.name}")
        print(f"System: {current_state.message}")

        #only assign preference_dict if its an INFORM act
        if dialog_act == "INFORM":
            preference_dict = extract_preferences(user_input)

        #logic for state transitions
        if current_state == welcome_state:      # Go to ask_area state if you do not know where the user wants to eat
            if dialog_act == "INFORM":
                # extract preferences
                # save / overwrite preferences
                # go next state
                if preference_dict[0] == "empty":
                    current_state = ask_area_state
                    return ask_area_state
        elif current_state == ask_area_state:   # Go to ask_food_state if you do not know what food the user wants to eat
            if dialog_act == "INFORM":
                if preference_dict[1] == "empty":
                    current_state == ask_food_state
                    return current_state
        elif current_state == ask_food_state:   # Go to ask_price state if you do not know what price the user wants to pay
            if dialog_act == "INFORM":
                if preference_dict[2] == "empty":
                    current_state == ask_price_state
                    return current_state
                
    
    def next_state(self, user_input):
        if self.state == "welcome":
            if user_input == "inform" or user_input == "null":
                self.state = "ask_area"
                print("System: In what area would you like to eat?")
                self.extract_preferences(user_input)
                self.response = False
                self.state = "ask_area" if not self.preferences["area"] else "ask_food_type"
            else:
                print("System: Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?")
        
        
        
        elif self.state == "ask_area":
            self.area = user_input
            self.state = "ask_food"
            print("System: What type of food are you looking for?")
        elif self.state == "ask_food":
            self.food_type = user_input
            self.state = "ask_price"
            print("System: What type of price range are you looking for?")
        elif self.state == "ask_price":
            self.price_range = user_input
            self.state = "double_check"
            print(f"System: So you want to eat at {self.area} place?")
        elif self.state == "double_check":
            if user_input == "yes":
                self.state = "suggest_restaurant"
                print(f"System: {self.restaurant} is a nice restaurant to eat at")
            else:
                self.state = "no_match"
                print("System: Sorry, such a restaurant does not exist")
        elif self.state == "suggest_restaurant":
            self.state = "give_info"
            print(f"System: The info for this restaurant is {self.other_options}")
        elif self.state == "give_info":
            self.state = "endstate"
            print("System: The conversation has ended.")
        elif self.state == "no_match":
            self.state = "endstate"
            print("System: The conversation has ended.")
        else:
            self.state = "endstate"
            print("System: The conversation has ended.")
    

    def next_state(self, user_input):

        self.handle_state(dialog_act, user_input)


    def run(self, model, vectorizer):
        if self.state == "welcome":
            print("hi")
            return None
        print("System: Hello , welcome to the Cambridge restaurant system? You can ask for restaurants by area , price range or food type . How may I help you?")
        while self.state != "endstate":
            user_input = input("You: ").lower()
            vectorized_user_input = vectorizer.transform([user_input])
            #classifying user input using ML model
            dialog_act = model.predict(vectorized_user_input)
            self.next_state(user_input)


            # if self.response:
                
            # else:
            #     user_input = ""
            #     self.response = True
            #     self.next_state(user_input)