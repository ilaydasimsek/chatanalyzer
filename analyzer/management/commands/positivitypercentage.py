import json

from django.core.management.base import BaseCommand
from analyzer.management.calculations.positivitycalculator import PositivityCalculator
from analyzer.models import UserStatistics, User


class Command(BaseCommand):
    help = 'Calculates the percentage messages that are positive for a user. Takes username as argument.'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs="+", type=str)

    def handle(self, *args, **options):
        username = options['username'][0]
        positivity_statistics = PositivityCalculator.get_positivity(username)
        self.update_db(positivity_statistics, username)
        print("User {}'s messages are {}% positive.".format(username, positivity_statistics))

    @staticmethod
    def update_db(positivity_statistics, username):
        user = User.objects.get(username=username)
        user_stat_object = UserStatistics.objects.get_or_create(user=user)[0]
        user_stat_object.positivity_percentage = positivity_statistics
        user_stat_object.save()
