import sys
import os
import pickle
from state_diagram import State_diagram
from functions import *


def main():
    with open(r'part_one/trained_models/lr_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    # Load the vectorizer
    with open(r'part_one/vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    state_diagram = State_diagram()
    state_diagram.run(model, vectorizer)


if __name__ == "__main__":
    main()
