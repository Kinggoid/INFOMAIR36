import pickle
from models.KeyWordMatching import KeywordMatchingModel
from models.majority_class import MajorityClassModel
from models.LogisticRegression import LogisticRegressionModel
from models.Decision_tree import DecisionTreeModel
from functions import datacleaning, vectorize

def main():
    file_path = 'part_one\\data\\dialog_acts.dat'
    X_train, X_test, y_train, y_test = datacleaning(file_path)

    # KEYWORDMATCHING -------------------------------------------------------------------
    km_model = KeywordMatchingModel(X_train)
    km_acc = km_model.evaluate(y_train)
    print("Keyword matching model accuracy is ", km_acc)

    # Save the keyword matching model
    with open(r'part_one/trained_models/km_model.pkl', 'wb') as f:
        pickle.dump(km_model, f)

    # MAJORITY CLASS ------------------------------------------------------------------
    mc = MajorityClassModel(y_train)
    mc_acc = mc.evaluate(X_test, y_test)
    print("Majority class model accuracy is ", mc_acc)

    # Save the majority class model
    with open(r'part_one/trained_models/mc_model.pkl', 'wb') as f:
        pickle.dump(mc, f)

    vectorizer, X_train, X_test = vectorize(X_train, X_test)

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

    # Save the logistic regression model
    with open(r'part_one/trained_models/lr_model.pkl', 'wb') as f:
        pickle.dump(lr_model, f)

    # DECISION TREE CLASSIFIER ---------------------------------------------------------
    dt_model = DecisionTreeModel()
    dt_model.fit(X_train, y_train)
    dt_model.evaluate(X_test, y_test)

    # Save the decision tree model
    with open(r'part_one/trained_models/dt_model.pkl', 'wb') as f:
        pickle.dump(dt_model, f)


if __name__ == "__main__":
    main()