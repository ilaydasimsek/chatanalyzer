import json

from django.core.management.base import BaseCommand

from analyzer.management.calculations.textlengthcalculator import TextLengthCalculator
from analyzer.models import User, UserStatistics


class Command(BaseCommand):
    help = 'gives you the average text length of a user'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=int)

    def handle(self, *args, **options):
        username = options['username'][0]
        length_statistics = TextLengthCalculator.text_length_statistics(username)
        self.update_db(length_statistics, username)
        print("User {} writes {} messages!".format(username, length_statistics))

    @staticmethod
    def update_db(length_statistics, username):
        user = User.objects.get(username=username)
        user_stat_object = UserStatistics.objects.get_or_create(user=user)[0]
        user_stat_object.avg_text_length = json.dumps(length_statistics)
        user_stat_object.save()
