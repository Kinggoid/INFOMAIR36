from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import pickle

def datacleaning(file_path):
    
    df = pd.read_csv(file_path, delimiter='\t')
    df.columns = ['dialog_act']

    # Cleaning dataset
    # Cleaning dataset
    df_clean = df.drop_duplicates()

    # Adding structure to database, separating dialog_acts and utterances
    df_clean = df_clean.copy()  # Create a deep copy to avoid SettingWithCopyWarning
    # Adding structure to database, separating dialog_acts and utterances
    df['utterance'] = df['dialog_act'].str.split().str[1:]
    df['dialog_act'] = df['dialog_act'].str.split().str[0]

    df_clean['utterance'] = df_clean['dialog_act'].str.split().str[1:]
    df_clean['dialog_act'] = df_clean['dialog_act'].str.split().str[0]

    # Converting to lists
    utterance_clean = df_clean['utterance'].tolist()  
    label_clean = df_clean['dialog_act'].tolist()  

    # Splitting data into training and test data
    utterance_clean_train, utterance_clean_test, label_clean_train, label_clean_test = train_test_split(
        utterance_clean, label_clean, test_size=0.15, random_state=42
    )

    return utterance_clean_train, utterance_clean_test, label_clean_train, label_clean_test


def vectorize(X_train, X_test):
    # Flatten each sublist in X_train and X_test by joining the strings with a space
    X_train_flat = [' '.join(doc) for doc in X_train]
    X_test_flat = [' '.join(doc) for doc in X_test]

    # Initialize the TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the training data
    X_train_tfidf = vectorizer.fit_transform(X_train_flat)

    # Transform the test data
    X_test_tfidf = vectorizer.transform(X_test_flat)

    # Return the transformed data
    return vectorizer, X_train_tfidf, X_test_tfidf