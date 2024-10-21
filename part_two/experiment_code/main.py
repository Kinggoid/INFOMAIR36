import pickle
from state_diagram import State_diagram
from utils import *
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def main():
    # Ask the user if the dialog should be formal or informal
    while True:
        dialog_style = input("Do you want the dialog to be formal or informal? (You can switch this during the dialog) (formal/informal): ").lower()
        if dialog_style in ['formal', 'informal']:
            formal = (dialog_style == 'formal')
            break
    print("\n")
    
    with open(r'part_one/trained_models/lr_model.pkl', 'rb') as f:
        model = pickle.load(f)
        vectorize = True
    
    # Load the vectorizer
    with open(r'part_one/vectorizer.pkl', 'rb') as f:
        vectorized = pickle.load(f)
    
    # Initialize and run the state diagram
    state_diagram = State_diagram()
    state_diagram.run(model, vectorized, vectorize, formal=formal)

if __name__ == "__main__":
    main()