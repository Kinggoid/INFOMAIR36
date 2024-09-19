from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score


class DecisionTreeModel:
    def __init__(self, random_state=42):
        # Initialize the Decision Tree Classifier
        self.model = DecisionTreeClassifier(random_state=random_state)

    def fit(self, X_train, y_train):
        # Train the model
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        # Make predictions on the test set
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_test):
        # Make predictions
        y_pred = self.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy}\n")

        # Evaluation report
        print(classification_report(y_test, y_pred))
