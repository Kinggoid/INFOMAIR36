import sys
import os
import pickle
from state_diagram import State_diagram
from functions import *


def main():
    # Ask the user for the classification method
    print("Choose the classification method:")
    print("1. Majority")
    print("2. Keyword Matching")
    print("3. Logistic Regression")
    choice = input("Enter the number of your choice: ")

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'part_one')))


    if choice == '1':
        with open(r'part_one/trained_models/mc_model.pkl', 'rb') as f:
            model = pickle.load(f)
    elif choice == '2':
        with open(r'part_one/trained_models/km_model.pkl', 'rb') as f:
            model = pickle.load(f)
    elif choice == '3':
        with open(r'part_one/trained_models/lr_model.pkl', 'rb') as f:
            model = pickle.load(f)
    else:
        print("Invalid choice. Defaulting to Logistic Regression.")
        with open(r'part_one/trained_models/lr_model.pkl', 'rb') as f:
            model = pickle.load(f)
    
    # Load the vectorizer
    with open(r'part_one/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    state_diagram = State_diagram()
    state_diagram.run(model, vectorizer)


if __name__ == "__main__":
    main()
