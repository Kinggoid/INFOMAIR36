from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from baselines import MajorityClassModel, KeywordMatchingModel
import pickle

# DATASET CLEANING -----------------------------------------------------------

# file_path = 'D:\School\MAIR\dialog_acts.dat'
file_path = 'part_one\dialog_acts.dat'
df = pd.read_csv(file_path, delimiter='\t')
df.columns = ['dialog_act']

# Cleaning dataset
df_clean = df.drop_duplicates()

# Adding structure to database, separating dialog_acts and utterances
df_clean = df_clean.copy()  # Create a deep copy to avoid SettingWithCopyWarning
df_clean['utterance'] = df_clean['dialog_act'].str.split().str[1:]
df_clean['dialog_act'] = df_clean['dialog_act'].str.split().str[0]

# Converting to lists
utterance_clean = df_clean['utterance'].tolist()  
label_clean = df_clean['dialog_act'].tolist()  

# Splitting data into training and test data
utterance_clean_train, utterance_clean_test, label_clean_train, label_clean_test = train_test_split(
    utterance_clean, label_clean, test_size=0.15, random_state=42
)

# BASELINE MODELS ======================================================================

# Initialize and evaluate Majority class
mc_model = MajorityClassModel(label_clean_train)

# testing performance
mc_acc = mc_model.evaluate(utterance_clean_test, label_clean_test)
print("Majority class model accuracy is", mc_acc)

# initialize and evaluate keyword matching
km_model = KeywordMatchingModel(utterance_clean_train, label_clean_train)

#testing performance
km_acc = km_model.evaluate(utterance_clean_test, label_clean_test)
print("Keyword matching model accuracy is ", km_acc)