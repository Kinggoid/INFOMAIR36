#import libraries
import pandas as pd
from sklearn.model_selection import train_test_split

print('-------------------------------')
#read dataset
# file_path = 'D:\School\MAIR\dialog_acts.dat'
file_path = 'part_one/dialog_acts.dat'
df = pd.read_csv(file_path, delimiter='\t')
df.columns = ['dialog_act']

# Cleaning dataset
df_clean = df.drop_duplicates()

print('1')

# Adding structure to dataset, separating dialog_acts and utterances
df['utterance'] = df['dialog_act'].str.split().str[1:]
df['dialog_act'] = df['dialog_act'].str.split().str[0]

print(df['utterance'].head())
print(df['dialog_act'].head())


print('2')

# Using .loc to avoid SettingWithCopyWarning
df_clean.loc[:, 'utterance'] = df_clean['dialog_act'].str.split().str[1:]
df_clean.loc[:, 'dialog_act'] = df_clean['dialog_act'].str.split().str[0]

print('3')

# Splitting data into train and test sets
X = df['utterance']
y = df['dialog_act']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

print('4')

# Doing the same for the clean dataset
X_clean = df_clean['utterance']
y_clean = df_clean['dialog_act']
Xc_train, Xc_test, yc_train, yc_test = train_test_split(X_clean, y_clean, test_size=0.15)

print('5')
print(yc_train.head())


class MajorityClassModel:
    # initialize model with training labels
    def __init__(self, labels):
        # set majority class as the label that has the highest occurence in the list
        self.majorityClass = max(labels,key=labels.count())

    # assigns majority class label to input data
    def test(self, input):
        return self.majorityClass
    
    # evaluates model based on lists of test data and labels 
    def evaluate(self, data, labels):
        if len(data) != len(labels):
            raise Exception("data and label lists are not the same size")
        
        # calculate accuracy of model
        correct = 0
        for i in range(0, len(data)):
            if self.test(data[i]) == labels[i]:
                correct += 1
        
        # return accuracy
        return correct / len(data)
    

classifier = MajorityClassModel(yc_train)