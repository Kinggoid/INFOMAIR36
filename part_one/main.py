from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from baselines import MajorityClassModel, KeywordMatchingModel
import pickle

# DATASET CLEANING -----------------------------------------------------------

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
utterances = df['utterance']
labels = df['dialog_act']
utterance_train, utterance_test, label_train, label_test = train_test_split(utterances, labels, test_size = 0.15)

#doing the same for the clean dataset
utterance_clean = df_clean['utterance']
label_clean = df_clean['dialog_act']
utterance_clean_train, utterance_clean_test, label_clean_train, label_clean_test = train_test_split(utterance_clean, label_clean, test_size = 0.15)


mc_model =  MajorityClassModel(utterance_clean_train)
# km_model =  KeywordMatchingModel(train_labels)

# get accuracies
mc_acc = mc_model.evaluate(utterance_clean_test, label_clean_test)
print("Majority class model accuracy is", mc_acc)

# km_acc = km_model.evaluate(test_insts, test_labels)
# print("Keyword matching model accuracy is", km_acc)