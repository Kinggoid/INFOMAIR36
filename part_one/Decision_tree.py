from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

#read dataset
# file_path = 'D:\School\MAIR\dialog_acts.dat'
file_path = 'part_one\dialog_acts.dat'
df = pd.read_csv(file_path, delimiter= '\t')
df.columns = ['dialog_act']

#cleaning dataset
df_clean = df.drop_duplicates()

#adding structure to database, separating dialog_acts and utterances
df['utterance'] = df['dialog_act'].str.split().str[1:]
df['dialog_act'] = df['dialog_act'].str.split().str[0]
df_clean['utterance'] = df_clean['dialog_act'].str.split().str[1:]
df_clean['dialog_act'] = df_clean['dialog_act'].str.split().str[0]

print(df['utterance'].head())
print(type(df['utterance'].loc[0]))

print(df['dialog_act'].head())
print(type(df['dialog_act'].loc[0]))

#join the words back into strings
df['utterance'] = df['utterance'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)
df_clean['utterance'] = df_clean['utterance'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)


def DTC(dataframe):

    #initializing vectorizing function, ngram range is 1 and 2. 1 for unique words and 2 for word relations like good and not good.
    vectorizer = CountVectorizer(ngram_range = (1,2), stop_words = 'english')

    #vectorizing the X set
    X = vectorizer.fit_transform(dataframe['utterance'])
    y = dataframe['dialog_act']

    #split data into train and test splits
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)
    print(type(X_train))
    #initialize decision tree classifier and fit to the data
    dtc = DecisionTreeClassifier(random_state=42)
    dtc.fit(X_train, y_train)

    #make predictions with the model to then test accuracy
    y_pred = dtc.predict(X_test)

    #evaluate the models performance
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))


print('-------------------------------')
DTC(df_clean)