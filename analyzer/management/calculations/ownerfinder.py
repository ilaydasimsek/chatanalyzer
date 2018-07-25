import pickle
from nltk.tokenize import word_tokenize
from analyzer.management.calculations.voteclassifier import VoteClassifier


class OwnerFinder():


    @classmethod
    # returns a tuple of classifying result and confidence level (between 0-1)
    def find_owner(cls, text):

        features = cls.find_features(text)
        if features == "unknown":
            return (-1, -1)

        voted_classifier = VoteClassifier.create_vote_classifier(cls.TRAINDATA_FILE_PATH)
        return (voted_classifier.classify(features), voted_classifier.confidence(features))
    @staticmethod
    def find_features(text):
        TRAINDATA_FILE_PATH = "analyzer/trained_data/ownerfinder_pickles/"
        word_features8k_f = open(TRAINDATA_FILE_PATH+"word_features8k.pickle", "rb")
        word_features = pickle.load(word_features8k_f)
        word_features8k_f.close()

        words = word_tokenize(text)
        features = {}
        is_found = 0
        for word in word_features:
            features[word] = (word in words)
            if word in words:
                is_found = 1  # changes is_found to 1 if any of the words in the sentence can be classifies into a user
        if is_found:
            return features
        else:
            return "unknown"
