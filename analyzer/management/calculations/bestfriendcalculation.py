import json
from math import sqrt

from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, get_list_or_404

from analyzer.models import UserStatistics, User


class BestFriendCalculation:
    # chooses the best k fits for user using k neighbors algorithm
    def __init__(self, k, username):
        self.k = k
        self.username = username

    def find_best_friends(self):
        user_stats = self.get_this_users_stats()
        all_user_stats = self.get_all_users_stats_except()
        friend_compatibility_list = list()
        for friend_stats in all_user_stats:
            compatibility_percentage = max(100 - self.find_total_distance(user_stats, friend_stats), 0)
            # smaller the distance higher the compatibility

            friend_compatibility_list.append((round(compatibility_percentage, 2), friend_stats.user.username))

        friend_compatibility_list.sort(reverse=True)
        return friend_compatibility_list[:self.k]

    # decodes the encoded json lists in UserStatistics, returns a dictionary of all stats
    @staticmethod
    def decode_stats(user_stats_obj):
        stat_dictionary = {'positivity_percentage': user_stats_obj.positivity_percentage}
        avg_time = json.loads(user_stats_obj.avg_time)
        avg_text_length = json.loads(user_stats_obj.avg_text_length)
        stat_dictionary['avg_time'] = avg_time
        stat_dictionary['avg_text_length'] = avg_text_length
        return stat_dictionary

    def get_all_users_stats_except(self):
        this_user = get_object_or_404(User, username=self.username)
        all_user_stats = get_list_or_404(UserStatistics, ~Q(user=this_user))
        print(all_user_stats)
        return all_user_stats

    def get_this_users_stats(self):
        this_user = get_object_or_404(User, username=self.username)
        this_user_stats = get_object_or_404(UserStatistics, user=this_user)
        return this_user_stats

    @staticmethod
    def find_distance_of_two_dicts(dict1, dict2):
        total = 0
        for key, dict1_value in dict1.items():
            dict2_value = dict2[key]
            total += (dict2_value - dict1_value) ** 2

        return total / 5

    # finds the length difference between two users
    def find_total_distance(self, user_stats_dict, friend_stats_dict):
        user_stats_dict = self.decode_stats(user_stats_dict)
        friend_stats_dict = self.decode_stats(friend_stats_dict)
        avg_positivity_distance = (user_stats_dict['positivity_percentage'] - friend_stats_dict[
            'positivity_percentage']) ** 2

        avg_length_distance = self.find_distance_of_two_dicts(
            user_stats_dict['avg_text_length'],
            friend_stats_dict['avg_text_length']
        )

        avg_time_distance = self.find_distance_of_two_dicts(
            user_stats_dict['avg_time'],
            friend_stats_dict['avg_time']
        )

        total = avg_length_distance + avg_positivity_distance + avg_time_distance
        return sqrt(total)
