# logistic_regression_classifier.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def run_logistic_regression(df):

    # Split into features (U) and labels (d)
    U = df["utterance"]  # The dialog utterances (X)
    d = df["dialog_act"] # The dialog act labels (y)

    # Initialize CountVectorizer instance
    vectorizer = CountVectorizer()
    
    # Transform utterances to word count vector
    U_bow = vectorizer.fit_transform(U)
    # print(U_bow.toarray()) # Word count vector matrix of dataset
    # print(vectorizer.vocabulary_) # Word to index mapping

    # Split dataset (85% training, 15% testing)
    U_train, U_test, d_train, d_test = train_test_split(U_bow, d, test_size=0.15, random_state=42)

    # Initialize and train the Logistic Regression model
    model = LogisticRegression()
    model.fit(U_train, d_train)

    # Make predictions on the test set
    d_pred = model.predict(U_test)

    # Calculate accuracy
    accuracy = accuracy_score(d_test, d_pred)
    print(f"Accuracy: {accuracy}\n")

    # Print a classification report for detailed results
    print(classification_report(y_test, y_pred))
    
    return model  # Optionally return the model for future use
