class MajorityClassModel:
    # Initialize model with training labels
    def __init__(self, labels):
        # Save labels for evaluate_ours method
        self.labels = labels
        # Set majority class as the label that has the highest occurrence
        self.majorityClass = max(labels, key=labels.count)

    # Assigns majority class label to input data
    def test(self, input):
        return self.majorityClass
    
    # Evaluates model based on lists of test data and labels
    def evaluate(self, data, labels):
        # Ensure that data and labels are both lists
        data = list(data)
        labels = list(labels)

        if len(data) != len(labels):
            raise Exception("Data and label lists are not the same size")

        correct = 0
        for i in range(len(data)):
            if self.test(data[i]) == labels[i]:
                correct += 1
        
        return correct / len(data)
        
    def evaluate_ours(self, data, labels):
        
        training_accuracy = sum(labels == self.majorityClass) / len(labels)

        return training_accuracy

# model that assigns labels to data based on keyword matching rules
class KeywordMatchingModel(MajorityClassModel):
    def __init__(self, labels):
        super().__init__(labels)

    def test(self, input):
        if "thank" in input:
            return "thankyou"
        elif "bye" in input:
            return "bye"
        elif "hi " in input or "hello" in input or "helo " in input:
            return "hello"
        elif "what" in input or "phone" in input or "address" in input:
            return "request"
        elif "yes" in input:
            return "affirm"
        elif "no" in input:
            return "negate"
        elif "looking" in input or "area" in input:
            return "inform"
        elif "else" in input:
            return "reqalts"
        else: 
            return self.majorityClass