import json
import os

from django.utils import timezone
from django.core.management.base import BaseCommand

from analyzer.management.calculations.answertimecalculator import AnswerTimeCalculator
from analyzer.management.calculations.positivitycalculator import PositivityCalculator
from analyzer.management.calculations.textlengthcalculator import TextLengthCalculator
from analyzer.models import Message, User, UserStatistics

from nltk.tokenize import sent_tokenize
import random

from chatanalyzer import settings

TOLERANCE = 1
MAX_ITERATION = 100


class Command(BaseCommand):
    help = 'partitions the data in database into specified number of bins'

    def handle(self, *args, **options):
        print("Process started.")
        self.create_users()
        self.save_messages()
        self.save_user_statistics()

    def create_users(self):
        user_friend_lists = [
            [2, 3, 4], [1, 5, 6], [1, 5, 7],
            [1, 5, 6, 7], [2, 3, 4], [2, 4, 9],
            [3, 4, 8], [7, 9], [6, 8]
        ]
        for i in range(1, 10):
            new_user = User()
            new_user.username = str(i)
            new_user.set_password('password123')
            new_user.first_name = str(i)
            new_user.last_name = str(i)
            new_user.email_address = 'default@email.com'
            new_user.friend_list = json.dumps(user_friend_lists[i-1])
            new_user.save()
            print("User {} is created".format(i))

    def save_messages(self):

        self.save_message_to_users(1, 2, 1, 1, 4, 2, 6, 1)
        self.save_message_to_users(1, 3, 1, 1, 4, 3, 7, 1)
        self.save_message_to_users(1, 4, 1, 1, 4, 4, 8, 1)
        self.save_message_to_users(2, 1, 1, 2, 6, 1, 4, 1)
        self.save_message_to_users(2, 5, 1, 2, 6, 5, 9, 1)
        self.save_message_to_users(2, 6, 1, 2, 6, 6, 10, 1)
        self.save_message_to_users(3, 1, 1, 3, 7, 1, 4, 1)
        self.save_message_to_users(3, 5, 1, 3, 7, 5, 9, 1)
        self.save_message_to_users(3, 7, 1, 3, 7, 7, 11, 1)
        self.save_message_to_users(4, 1, 1, 4, 8, 1, 4, 1)
        self.save_message_to_users(4, 5, 1, 4, 8, 5, 9, 1)
        self.save_message_to_users(4, 6, 1, 4, 8, 6, 10, 1)
        self.save_message_to_users(4, 7, 1, 4, 8, 7, 11, 1)
        self.save_message_to_users(5, 2, 1, 5, 9, 2, 6, 1)
        self.save_message_to_users(5, 3, 1, 5, 9, 3, 7, 1)
        self.save_message_to_users(5, 4, 1, 5, 9, 4, 8, 1)
        self.save_message_to_users(6, 2, 1, 6, 10, 2, 6, 1)
        self.save_message_to_users(6, 4, 1, 6, 10, 4, 8, 1)
        self.save_message_to_users(6, 9, 1, 6, 10, 9, 13, 1)
        self.save_message_to_users(7, 3, 1, 7, 11, 3, 7, 1)
        self.save_message_to_users(7, 4, 1, 7, 11, 4, 8, 1)
        self.save_message_to_users(7, 8, 1, 7, 11, 8, 12, 1)
        self.save_message_to_users(8, 7, 1, 8, 12, 7, 11, 1)
        self.save_message_to_users(8, 9, 1, 8, 12, 9, 13, 1)
        self.save_message_to_users(9, 6, 1, 9, 13, 6, 10, 1)
        self.save_message_to_users(9, 8, 1, 9, 13, 8, 12, 1)

    @staticmethod
    def save_user_statistics():
        users_set = User.objects.all()
        for user in users_set:
            length_statistics = TextLengthCalculator.text_length_statistics(user.username)
            print("Text length statistics for user {} is calculated.".format(user.username))
            positivity_statistics = PositivityCalculator.get_positivity(user.username)
            print("Positivity statistics for user {} is calculated.".format(user.username))
            time_statistics = AnswerTimeCalculator.answer_time_statistics(user.username)
            print("Time statistics for user {} is calculated.".format(user.username))
            user_stat_object = UserStatistics.objects.get_or_create(user=user)[0]
            user_stat_object.avg_time = json.dumps(time_statistics)
            user_stat_object.avg_text_length = json.dumps(length_statistics)
            user_stat_object.positivity_percentage = positivity_statistics
            user_stat_object.save()

    def save_message_to_users(self, user1, user2, time_delta, rand1low, rand1high, rand2low, rand2high, saveTo):
        last_time_delta = 0
        i = 0
        lines = self.get_from_file(user1, user2)
        print("Saving {} # of messages for user {}".format(len(lines), user1))
        for line in lines:
            user_val = random.randint(0, 1)
            if user_val == 0:
                user = User.objects.get(username=user1)
                receiver = User.objects.get(username=user2)
                rand_no = random.randint(rand1low, rand1high)
                i += 1
                if saveTo:
                    date = timezone.now() + timezone.timedelta(minutes=(last_time_delta + time_delta * user1 * rand_no))
                    last_time_delta = time_delta * user1 * rand_no + last_time_delta
                    message_object = Message(message_text=line, sender=user, receiver=receiver, date=date)
                    message_object.save()
                else:
                    last_time_delta = last_time_delta + time_delta * user1 * rand_no

            else:
                i += 1
                rand_no = random.randint(rand2low, rand2high)
                user = User.objects.get(username=user1)
                receiver = User.objects.get(username=user2)
                last_time_delta = last_time_delta + time_delta * user2 * rand_no
                date = timezone.now() + timezone.timedelta(minutes=(last_time_delta + time_delta * user1 * rand_no))
                last_time_delta = time_delta * user1 * rand_no + last_time_delta
                message_object = Message(message_text=line, sender=user, receiver=receiver, date=date)
                message_object.save()

        print("Completed.")

    @staticmethod
    def get_from_file(user1, user2):
        filename = "Conversation{}-{}.txt".format(user1, user2)
        file_path = os.path.join(settings.BASE_DIR, 'conversationFiles', filename)

        messages = open(file_path, encoding="utf8").read()
        lines = sent_tokenize(messages)

        return lines
