from collections import Counter
from analyzer.models import User, Message
import numpy as np
import warnings


class TextLengthCalculator:
    LENGTH_LIST = ['Very Short', 'Short', 'Medium', 'Long', 'Very Long']

    # calculates average text length using k nearest neighbors algorithm
    @classmethod
    def text_length_statistics(cls, username):
        message_list_size = 600  # number of messages that will be used for calculation
        train_set = np.load('analyzer/trained_data/length_train_data.npy').item()  # pre trained length information
        user = User.objects.get(username=username)
        message_list = Message.objects.filter(sender=user.id)[:message_list_size]
        dataset = []
        results = []
        for message in message_list:
            dataset.append((message.message_text, len(message.message_text)))

        for data in dataset:
            results.append(cls.k_nearest_neighbors(train_set, data, 8))
        message_stat = Counter(results).most_common(5)
        results = {}

        for i in range(0, len(message_stat)):
            results[message_stat[i][0]] = round(float(message_stat[i][1]) / message_list_size * 100, 3)

        # fills the non existent length values with zero
        for length_name in cls.LENGTH_LIST:
            key_exists = results.get(length_name, False)  # either returns the object or false
            if not key_exists:
                results[length_name] = float(0)

        return results

    @staticmethod
    def k_nearest_neighbors(data, predict, k=3):
        if len(data) >= k:
            warnings.warn('K is set to a value less than total voting groups')

        distances = []
        # features is a tuple of (message,length)
        for group in data:
            for features in data[group]:
                distance = abs(features[1] - predict[1])
                distances.append([distance, group])

        votes = [i[1] for i in sorted(distances)[:k]]
        result = Counter(votes).most_common(1)[0][0]
        return result
