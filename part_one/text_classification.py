#import libraries
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

# DATASET DESCRIPTION -----------------------------------------------------------

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

#splitting data into train and test data
X = df['utterance']
y = df['dialog_act']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.15)

#doing the same for the clean dataset
X_clean = df_clean['utterance']
y_clean = df_clean['dialog_act']
Xc_train, Xc_test, yc_train, yc_test = train_test_split(X_clean, y_clean, test_size = 0.15)

# BASELINE SYSTEMS -----------------------------------------------------------------

class Classifier:
    def __init__(self, utterance_train, utterance_test, dialog_train, dialog_test):
        self.dialog_test = dialog_test
        self.utterance_test = utterance_test
        self.dialog_train = dialog_train
        self.utterance_train = utterance_train

    def Majority_Class(self):
        majority_class = self.dialog_train.value_counts().idxmax()
        train_accuracy = sum(self.dialog_train == majority_class) / len(self.dialog_train)
        
        return majority_class, train_accuracy
    
    def Keyword_Matching(self):
        # Predicted dialog-label (empty table)
        predicted_dialog = pd.Series()

        # Look through utterances
        for utterance in self.utterance_train:       
            utterance_set = set(utterance)

            # If a certain key is in utterance, classify as:...
            if 'goodbye' in utterance_set or 'bye' in utterance_set:
                label = pd.Series('bye')
            elif 'thank' in utterance_set:
                label = pd.Series('thankyou')
            elif 'hi ' in utterance_set or "hello" in utterance_set or "helo " in utterance_set:
                label = pd.Series('hello')
            elif 'what ' in utterance_set or 'phone ' in utterance_set or 'address ' in utterance_set:
                label = pd.Series('request')
            elif 'yes' in utterance_set:
                label = pd.Series('affirm')
            elif 'no' in utterance_set:
                label = pd.Series('negate')
            elif 'area ' in utterance_set or 'looking ' in utterance_set:
                label = pd.Series('inform')
            elif 'else ' in utterance_set:
                label = pd.Series('reqalts')
            else:
                label = pd.Series('inform')
            
            # Add to prediction table
            predicted_dialog = pd.concat([predicted_dialog, label], ignore_index=True)
        
        # Accuracy
        predicted_dialog.index = self.dialog_train.index
        train_accuracy = sum(self.dialog_train == predicted_dialog) / len(self.dialog_train)

        return predicted_dialog, train_accuracy

classifier = Classifier(Xc_train, Xc_test, yc_train, yc_test)
print(classifier.Majority_Class())
predicted_dialog, train_accuracy = classifier.Keyword_Matching()
print(train_accuracy)

classifier = Classifier(X_train, X_test, y_train, y_test)
print(classifier.Majority_Class())
predicted_dialog, train_accuracy = classifier.Keyword_Matching()
print(train_accuracy)