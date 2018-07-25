from nltk.classify import ClassifierI
from collections import Counter
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
import nltk

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers

    # takes the vote from each classifier and returns most common vote
    def classify(self, features):
        votes = list()
        for c in self._classifiers:
            vote = c.classify(features)
            votes.append(vote)
        vote_count_dict = Counter(votes).most_common(5)
        return vote_count_dict[0][0]  # if there is a tie in terms of votes returns one of the most common

        # same as classify() but returns confidence level (between 0-1)

    def confidence(self, features):
        votes = list()
        for c in self._classifiers:
            vote = c.classify(features)
            votes.append(vote)
        vote_count_dict = Counter(votes).most_common(5)
        choice = vote_count_dict[0][0]
        choice_votes = votes.count(choice)
        return choice_votes / len(votes)

    @staticmethod
    def create_vote_classifier(file_path):
        open_file = open(file_path+"originalnaivebayes.pickle", "rb")
        classifier = pickle.load(open_file)
        open_file.close()

        open_file = open(file_path+"MNB_classifier.pickle", "rb")
        MNB_classifier = pickle.load(open_file)
        open_file.close()

        open_file = open(file_path+"LogisticRegression_classifier.pickle", "rb")
        LogisticRegression_classifier = pickle.load(open_file)
        open_file.close()

        open_file = open(file_path+"LinearSVC_classifier.pickle", "rb")
        LinearSVC_classifier = pickle.load(open_file)
        open_file.close()

        open_file = open(file_path+"SGDC_classifier.pickle", "rb")
        SGDC_classifier = pickle.load(open_file)
        open_file.close()

        voted_classifier = VoteClassifier(classifier,
                                          MNB_classifier,
                                          LogisticRegression_classifier,
                                          LinearSVC_classifier,
                                          SGDC_classifier)
        return voted_classifier

    @staticmethod
    def save_classifiers(file_path, featuresets):
        training_set = featuresets[:16000]
        testing_set = featuresets[16000:]

        classifier = nltk.NaiveBayesClassifier.train(training_set)
        print("Original Naive Bayes Accuracy: ", nltk.classify.accuracy(classifier, testing_set) * 100)
        classifier.show_most_informative_features(100)

        save_classifier = open(file_path+"originalnaivebayes.pickle", "wb")
        pickle.dump(classifier, save_classifier)
        save_classifier.close()

        MNB_classifier = SklearnClassifier(MultinomialNB())
        MNB_classifier.train(training_set)
        print("MNB_classifier accuracy percent:", (nltk.classify.accuracy(MNB_classifier, testing_set)) * 100)

        save_classifier = open(file_path+"MNB_classifier.pickle", "wb")
        pickle.dump(MNB_classifier, save_classifier)
        save_classifier.close()

        LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
        LogisticRegression_classifier.train(training_set)
        print("LogisticRegression_classifier accuracy percent:",
              (nltk.classify.accuracy(LogisticRegression_classifier, testing_set)) * 100)

        save_classifier = open(file_path+"LogisticRegression_classifier.pickle", "wb")
        pickle.dump(LogisticRegression_classifier, save_classifier)
        save_classifier.close()

        LinearSVC_classifier = SklearnClassifier(LinearSVC())
        LinearSVC_classifier.train(training_set)
        print("LinearSVC_classifier accuracy percent:",
              (nltk.classify.accuracy(LinearSVC_classifier, testing_set)) * 100)

        save_classifier = open(file_path+"LinearSVC_classifier.pickle", "wb")
        pickle.dump(LinearSVC_classifier, save_classifier)
        save_classifier.close()

        SGDC_classifier = SklearnClassifier(SGDClassifier())
        SGDC_classifier.train(training_set)
        print("SGDClassifier accuracy percent:", nltk.classify.accuracy(SGDC_classifier, testing_set) * 100)

        save_classifier = open(file_path+"SGDC_classifier.pickle", "wb")
        pickle.dump(SGDC_classifier, save_classifier)
        save_classifier.close()


