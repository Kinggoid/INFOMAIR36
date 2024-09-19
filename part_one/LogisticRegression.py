# logistic_regression_classifier.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def run_logistic_regression(X_train, X_test, y_train, y_test):

    # Initialize and train the Logistic Regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    d_pred = model.predict(X_test)

    # Calculate accuracy (by hand)
    accuracy = accuracy_score(y_test, d_pred)
    print(f"Accuracy: {accuracy}\n")

    # Evaluation report:
    print(classification_report(y_test, d_pred))
    
