from models.KeyWordMatching import KeywordMatchingModel
from models.majority_class import MajorityClassModel
from models.LogisticRegression import LogisticRegressionModel
from models.Decision_tree import DecisionTreeModel
from functions import datacleaning, vectorize


def main():

    file_path = 'part_one\dialog_acts.dat'
    X_train, X_test, y_train, y_test = datacleaning(file_path)

    # KEYWORDMATCHING -------------------------------------------------------------------

    # initialize and evaluate keyword matching
    km_model = KeywordMatchingModel(X_train)

    #testing performance
    km_acc = km_model.evaluate(y_train)
    print("Keyword matching model accuracy is ", km_acc)


    # MAJORITY CLASS ------------------------------------------------------------------
    mc = MajorityClassModel(y_train)
    mc_acc = mc.evaluate(X_test, y_test)
    print("Majority class model accuracy is ", mc_acc)

    X_train, X_test = vectorize(X_train, X_test)


    # LOGISTIC REGRESSION --------------------------------------------------------------
    print('Logistic Regression df:')

    model = LogisticRegressionModel()
    model.fit(X_train, y_train)
    print(X_test[0])
    print(y_test[0])
    model.evaluate(X_test, y_test)


    # DECISION TREE CLASSIFIER ---------------------------------------------------------

    # if z == 4:
    model = DecisionTreeModel()
    model.fit(X_train, y_train)
    model.evaluate(X_test, y_test)
    

main()

    








