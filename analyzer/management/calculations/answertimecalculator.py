import json
import random
from collections import Counter
from django.db.models.query_utils import Q
from analyzer.models import User, Message
import numpy as np
import warnings


class AnswerTimeCalculator:
    LENGTH_LIST = ('Very Short', 'Short', 'Medium', 'Long', 'Very Long')

    @classmethod
    def answer_time_statistics(cls, username):
        message_list_size = 600
        train_set = np.load('analyzer/trained_data/time_train_data.npy').item()
        user = User.objects.get(username=username)
        friend_list = json.loads(user.friend_list)
        results = []

        for friend_name in friend_list:

            friend = User.objects.get(username=friend_name)
            messages = Message.objects.filter(
                Q(sender=user.id, receiver=friend.id) | Q(sender=friend.id, receiver=user.id)).order_by('-date')[::-1]
            messages = messages[:message_list_size]
            for i in range(len(messages) - 1):
                current_message = messages[i]
                next_message = messages[i + 1]

                if (current_message.sender == friend and next_message.sender == user):
                    hour_diff = 60 * (current_message.date.hour - next_message.date.hour)
                    min_diff = (current_message.date.minute - next_message.date.minute)
                    sec_diff = (current_message.date.second - next_message.date.second) / 60
                    time_delta = abs(hour_diff + min_diff + sec_diff)
                    results.append(cls.k_nearest_neighbors(train_set, time_delta, 8))
        message_stat = Counter(results).most_common(5)
        total_counted = len(results)
        results = {}
        for i in range(0, len(message_stat)):
            results[message_stat[i][0]] = round(float(message_stat[i][1]) / total_counted * 100, 3)

        for length_name in cls.LENGTH_LIST:
            key_exists = results.get(length_name, False)  # either returns the object or false
            if (not (key_exists)):
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
                distance = abs(features - predict)
                distances.append([distance, group])

        votes = [i[1] for i in sorted(distances)[:k]]
        result = Counter(votes).most_common(1)[0][0]
        return result


    @staticmethod
    # creates random numbers in given ranges to train k means cluster algorithm
    def write_to_file():
        for i in range(0, 25000):
            print(str(random.uniform(0, 30)))
        for i in range(0, 25000):
            print(str(random.uniform(25, 60)))
        for i in range(0, 25000):
            print(str(random.uniform(50, 110)))
        for i in range(0, 25000):
            print(str(random.uniform(110, 200)))
