import pickle
from models.KeyWordMatching import KeywordMatchingModel
from models.majority_class import MajorityClassModel
from models.LogisticRegression import LogisticRegressionModel
from models.Decision_tree import DecisionTreeModel
from functions import datacleaning, vectorize

import warnings
warnings.filterwarnings('ignore')

def main():
    file_path = 'part_one\\data\\dialog_acts.dat'
    X_train, X_test, y_train, y_test, X_train_nonclean, X_test_nonclean, y_train_nonclean, y_test_nonclean = datacleaning(file_path)


    # KEYWORDMATCHING -------------------------------------------------------------------
    km_model = KeywordMatchingModel(X_train)
    km_acc = km_model.evaluate(y_train)
    print(X_train[0])
    print("Keyword matching model accuracy is ", km_acc)

    km_model_nonclean = KeywordMatchingModel(X_train_nonclean)
    km_acc_nonclean = km_model_nonclean.evaluate(y_train_nonclean)
    print(X_train_nonclean[0])
    print("nonclean Keyword matching model accuracy is ", km_acc_nonclean)

    # Save the keyword matching model
    with open(r'part_one/trained_models/km_model.pkl', 'wb') as f:
        pickle.dump(km_model, f)

    # MAJORITY CLASS ------------------------------------------------------------------
    mc = MajorityClassModel(y_train)
    mc_acc = mc.evaluate(X_test, y_test)
    print("Majority class model accuracy is ", mc_acc)

    mc_nonclean = MajorityClassModel(y_train_nonclean)
    mc_acc_nonclean = mc_nonclean.evaluate(X_test_nonclean, y_test_nonclean)
    print("nonclean Majority class model accuracy is ", mc_acc_nonclean)

    # Save the majority class model
    with open(r'part_one/trained_models/mc_model.pkl', 'wb') as f:
        pickle.dump(mc, f)

    vectorizer, X_train, X_test = vectorize(X_train, X_test)
    vectorizer_nonclean, X_train_nonclean, X_test_nonclean = vectorize(X_train_nonclean, X_test_nonclean)

    # Save the vectorizer
    with open(r'part_one/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)

    # LOGISTIC REGRESSION --------------------------------------------------------------
    print('Logistic Regression df:')
    lr_model = LogisticRegressionModel()
    lr_model.fit(X_train, y_train)
    print(X_test[0])
    print(y_test[0])
    lr_model.evaluate(X_test, y_test)

    print('nonclean Logistic Regression df:')
    lr_model_nonclean = LogisticRegressionModel()
    lr_model_nonclean.fit(X_train_nonclean, y_train_nonclean)
    print(X_test_nonclean[0])
    print(y_test_nonclean[0])
    lr_model_nonclean.evaluate(X_test_nonclean, y_test_nonclean)

    # Save the logistic regression model
    with open(r'part_one/trained_models/lr_model.pkl', 'wb') as f:
        pickle.dump(lr_model, f)

    # DECISION TREE CLASSIFIER ---------------------------------------------------------
    print('Decision Tree Classifier df:')
    dt_model = DecisionTreeModel()
    dt_model.fit(X_train, y_train)
    dt_model.evaluate(X_test, y_test)

    print('nonclean Decision Tree Classifier df:')
    dt_model_nonclean = DecisionTreeModel()
    dt_model_nonclean.fit(X_train_nonclean, y_train_nonclean)
    dt_model_nonclean.evaluate(X_test_nonclean, y_test_nonclean)

    # Save the decision tree model
    with open(r'part_one/trained_models/dt_model.pkl', 'wb') as f:
        pickle.dump(dt_model, f)


if __name__ == "__main__":
    main()