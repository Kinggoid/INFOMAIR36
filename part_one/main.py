from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from baselines import MajorityClassModel, KeywordMatchingModel
import pickle
from LogisticRegression import run_logistic_regression

# DATASET CLEANING ---------------------------------------------------------------

# File_path = 'D:\School\MAIR\dialog_acts.dat'
file_path = 'part_one\dialog_acts.dat'
df = pd.read_csv(file_path, delimiter='\t')
df.columns = ['dialog_act']

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

# First, make sure that the utterance column is a string (not a list of words)
df['utterance'] = df['utterance'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)
df_clean['utterance'] = df_clean['utterance'].apply(lambda x: ' '.join(x) if isinstance(x, list) else x)

# Splitting data into training and test data
utterance_clean_train, utterance_clean_test, label_clean_train, label_clean_test = train_test_split(
    utterance_clean, label_clean, test_size=0.15, random_state=42
)

# Doing the same for the clean dataset
utterance_clean = df_clean['utterance']
label_clean = df_clean['dialog_act']
utterance_clean_train, utterance_clean_test, label_clean_train, label_clean_test = train_test_split(utterance_clean, label_clean, test_size = 0.15)


# BASELINE MODELS -----------------------------------------------------------------

# Initialize and evaluate Majority class
# mc_model = MajorityClassModel(label_clean_train)

# # Testing performance
# mc_acc = mc_model.evaluate(utterance_clean_test, label_clean_test)
# print("Majority class model accuracy is", mc_acc)

# initialize and evaluate keyword matching
km_model = KeywordMatchingModel(utterance_clean)

#testing performance
km_acc = km_model.evaluate(label_clean)
print("Keyword matching model accuracy is ", km_acc)

# km_acc = km_model.evaluate(test_insts, test_labels)
# print("Keyword matching model accuracy is", km_acc)

# LOGISTIC REGRESSION --------------------------------------------------------------

run_logistic_regression(df)
run_logistic_regression(df_clean)

