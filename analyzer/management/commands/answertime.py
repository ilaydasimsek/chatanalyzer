import json
from analyzer.models import User, UserStatistics
from django.core.management.base import BaseCommand
from analyzer.management.calculations.answertimecalculator import AnswerTimeCalculator


class Command(BaseCommand):
    help = 'calculates the average answer time of given user. Takes username as argument'

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)

    def handle(self, *args, **options):
        username = options['username'][0]
        time_statistics = AnswerTimeCalculator.answer_time_statistics(username)
        self.update_db(time_statistics, username)
        print(time_statistics)

    @staticmethod
    def update_db(time_statistics, username):
        user = User.objects.get(username=username)
        user_stat_object = UserStatistics.objects.get_or_create(user=user)[0]
        user_stat_object.avg_time = json.dumps(time_statistics)
        user_stat_object.save()
