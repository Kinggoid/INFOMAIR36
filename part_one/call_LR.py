# main.py
from LogisticRegression import run_logistic_regression

if __name__ == "__main__":
    
    # Sample dialog_acts data
    data = [
        ["inform", "im looking for a moderately priced restaurant that serves"],
        ["inform", "any part of town"],
        ["inform", "bistro food"],
        ["confirm", "is there a moderately priced restaurant that serves british food"],
        ["affirm", "yes"],
        ["request", "could i get their phone number"],
        ["thankyou", "thank you good bye"],
        ["inform", "moderately priced restaurant in the south part of town"],
        ["inform", "any"],
        ["request", "address"],
        ["null", "code"],
        ["request", "postcode"],
        ["thankyou", "thank you goodbye"],
        ["inform", "cheap"],
        ["inform", "mediterranean"],
        ["request", "phone number"],
        ["bye", "goodbye"],
        ["inform", "im looking for a restaurant that serves seafood"],
        ["inform", "any"],
        ["request", "can i get the address and phone number"],
        ["thankyou", "thank you goodbye"],
        ["inform", "east"],
        ["inform", "expensive"],
        ["request", "could i have their phone number and the type of food"],
        ["inform", "expensive restaurant"],
        ["affirm", "yes"],
        ["request", "whats the phone number"],
        ["thankyou", "thank you good bye"],
    ]
    
    # Call the logistic regression function
    run_logistic_regression(data)