from nltk.corpus import stopwords
import random
import nltk
import pickle
from nltk.tokenize import word_tokenize, sent_tokenize

from analyzer.models import User, Message
from analyzer.management.calculations.voteclassifier import VoteClassifier


class ClassifyByOwner:
    TRAINDATA_FILE_PATH = "analyzer/trained_data/ownerfinder_pickles/"

    def __init__(self, message_list_size):
        self.message_list_size = message_list_size
        self.documents = list()
        self.all_words = list()

        self.stop_words = set(stopwords.words("english"))  # useless words like "for, a, the"
        self.stop_words.update(
            ["#", "$", ",", ".", '&', "(", ")", "\"", "'", "''", "...", "—"]
        )  # useless punctuation that might disrupt the analysis

    def classify_messages_for_user(self, username):
        user = User.objects.get(username=username)
        user_queryset = Message.objects.filter(sender=user).order_by('?')[:self.message_list_size]

        for messageObj in user_queryset:
            self.documents.append((messageObj.text, username))
            words = word_tokenize(messageObj.text)
            for w in words:
                if w not in self.stop_words:
                    self.all_words.append(w.lower())

    def create_dataset(self):
        users = User.objects.all()
        for user in users:
            self.classify_messages_for_user(user.username)
        random.shuffle(self.documents)

    @staticmethod
    def find_features(document, word_features):
        words = word_tokenize(document)
        features = {}
        for word in word_features:
            features[word] = word in words
        return features

    def classify_and_save(self):
        random.shuffle(self.documents)
        random.shuffle(self.all_words)

        save_documents = open(self.TRAINDATA_FILE_PATH + "documents.pickle", "wb")
        pickle.dump(self.documents, save_documents)
        save_documents.close()

        all_words = nltk.FreqDist(self.all_words)
        word_features = list(all_words.keys())[:8000]

        save_word_features = open(self.TRAINDATA_FILE_PATH + "word_features8k.pickle", "wb")
        pickle.dump(word_features, save_word_features)
        save_word_features.close()

        featuresets = [
            (self.find_features(msg, word_features), user_category)
            for (msg, user_category) in self.documents
        ]

        random.shuffle(featuresets)

        save_featuresets = open(self.TRAINDATA_FILE_PATH + "featuresets.pickle", "wb")
        pickle.dump(featuresets, save_featuresets)

        VoteClassifier.save_classifiers(self.TRAINDATA_FILE_PATH , featuresets)
