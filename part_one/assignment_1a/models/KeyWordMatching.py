# model that assigns labels to data based on keyword matching rules
class KeywordMatchingModel():
    def __init__(self, input):
        self.input = input
        self.classification = self._classify(input)

    def _classify(self, input):
        classification = []
        for i in range(len(input)):
            utterance = ' '.join(input[i])  # Join the words in each utterance into a string
            
            print(utterance)
            if "thank" in utterance:
                classification.append("thankyou")
            elif "bye" in utterance:
                classification.append("bye")
            elif "hi " in utterance or "hello" in utterance or "helo " in utterance:
                classification.append("hello")
            elif "what" in utterance or "phone" in utterance or "address" in utterance:
                classification.append("request")
            elif "yes" in utterance or "right" in utterance or "yeah" in utterance:
                classification.append("affirm")
            elif "no" in utterance or "nope" in utterance:
                classification.append("negate")
            elif "looking" in utterance or "area" in utterance or "food" in utterance:
                classification.append("inform")
            elif "else" in utterance:
                classification.append("reqalts")
            else: 
                classification.append("inform")
        return classification

    def evaluate(self, labels):
        correct = 0
        for i in range(len(labels)):
            if labels[i] == self.classification[i]:
                correct += 1
        training_accuracy = correct / len(labels)
        return training_accuracy
    
    def predict(self, input):
        return self._classify(input)