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
    
    def evaluate(self, data, labels):

        correct = 0

        for i in range(len(labels)):
            if labels[i] == self.majorityClass:
                correct += 1

        training_accuracy = correct / len(labels)

        return training_accuracy

# model that assigns labels to data based on keyword matching rules
class KeywordMatchingModel():
    def __init__(self, input):
        self.input = input

        self.classification = []

        for i in range(len(input)):
            utterance = ' '.join(input[i])  # Join the words in each utterance into a string
            
            if "thank" in utterance:
                self.classification.append("thankyou")
            elif "bye" in utterance:
                self.classification.append("bye")
            elif "hi " in utterance or "hello" in utterance or "helo " in utterance:
                self.classification.append("hello")
            elif "what" in utterance or "phone" in utterance or "address" in utterance:
                self.classification.append("request")
            elif "yes" in utterance or "right" in utterance or "yeah" in utterance:
                self.classification.append("affirm")
            elif "no" in utterance or "nope" in utterance:
                self.classification.append("negate")
            elif "looking" in utterance or "area" in utterance or "food" in utterance:
                self.classification.append("inform")
            elif "else" in utterance:
                self.classification.append("reqalts")
            else: 
                self.classification.append("inform")

    def evaluate (self, labels):
        correct = 0

        for i in range(len(labels)):
            if labels[i] == self.classification[i]:
                correct += 1

        training_accuracy = correct / len(labels)

        return training_accuracy