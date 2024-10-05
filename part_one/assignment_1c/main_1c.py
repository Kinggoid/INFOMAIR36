import sys
import os
import pickle
from state_diagram import State_diagram
from functions import *


def main():
    # Ask the user for the classification method
    print("Choose the classification method:")
    print("1. Keyword Matching")
    print("2. Logistic Regression")
    model_choice = input("Enter the number of your choice: ")

    while True:
        levenshtein_distance_choice = input("Please enter the desired Levenshtein distance (1-10): ")
        try:
            levenshtein_distance_choice = int(levenshtein_distance_choice)
            if 1 <= levenshtein_distance_choice <= 10:
                break
            else:
                levenshtein_distance_choice = input("Please enter a valid number between 1 and 10: ")
        except ValueError:
            levenshtein_distance_choice = input("Please enter a valid number between 1 and 10: ")

    while True:
        allow_dialog_restart = input("Allow dialog restarts? (y/n): ")
        if allow_dialog_restart == 'y' or allow_dialog_restart == 'n':
            break

    if model_choice == '1':
        with open(r'part_one/trained_models/km_model.pkl', 'rb') as f:
            model = pickle.load(f)
            vectorize = False
    elif model_choice  == '2':
        with open(r'part_one/trained_models/lr_model.pkl', 'rb') as f:
            model = pickle.load(f)
            vectorize = True
    else:
        print("Invalid choice. Defaulting to Logistic Regression.")
        with open(r'part_one/trained_models/lr_model.pkl', 'rb') as f:
            model = pickle.load(f)
            vectorize = True
    
    # Load the vectorizer
    with open(r'part_one/vectorizer.pkl', 'rb') as f:
        vectorized = pickle.load(f)
    

    state_diagram = State_diagram()
    state_diagram.run(model, vectorized, vectorize, levenshtein_distance_choice, allow_dialog_restart)


if __name__ == "__main__":
    main()
