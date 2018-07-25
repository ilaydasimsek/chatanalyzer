from analyzer.models import User, Message
from nltk.tokenize import word_tokenize
from analyzer.management.calculations.voteclassifier import VoteClassifier
import pickle


class PositivityCalculator():
    TRAINDATA_FILE_PATH = "analyzer/trained_data/positivity_pickles/"

    def __init__(self):
        self.allowed_word_types = ["J"]  # JJ, JJR, JJS -> adjective , comparative, superlative
    @classmethod
    def find_features(cls, document):
        words = word_tokenize(document)

        word_features6k_f = open(cls.TRAINDATA_FILE_PATH + "word_features.pickle", "rb")
        word_features = pickle.load(word_features6k_f)
        word_features6k_f.close()

        features = {}
        is_found = 0

        for w in word_features:
            features[w] = (w in words)
            if (w in words):
                is_found = 1

        if (is_found):
            return features
        else:
            return []

    @classmethod
    def sentiment_analysis(cls, text):
        features = cls.find_features(text)  # returns empty list if there isn't any pos or neg words in sentence
        if (features == []):
            return "unknown", 0
        voted_classifier = VoteClassifier.create_vote_classifier(cls.TRAINDATA_FILE_PATH)
        return (voted_classifier.classify(features), voted_classifier.confidence(features))

    @classmethod
    def get_positivity(cls, username):
        pos_messages = 0
        neg_messages = 0

        user = User.objects.get(username=username)
        messages = Message.objects.filter(sender=user).order_by("?")[:600]

        for message in messages:
            (className, confidence) = cls.sentiment_analysis(message.message_text)
            # does not classify as pos or neg if algorithms confidence<=0.6
            if className == 'pos' and confidence > 0.6:
                pos_messages += 1

            elif className == 'neg' and confidence > 0.6:
                neg_messages += 1

        pos_percentage = pos_messages / (pos_messages + neg_messages) * 100
        # rounds the digits after dot to 3
        return round(pos_percentage, 3)
