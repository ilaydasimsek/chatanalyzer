from django.core.management.base import BaseCommand

from analyzer.management.calculations.bestfriendcalculation import BestFriendCalculation

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type=str)
        parser.add_argument('k', nargs='+', type=int)

    def handle(self, *args , **options):
        username = options['username'][0]
        k = options['k'][0]
        calculator = BestFriendCalculation(k, username)
        print(calculator.find_best_friends())
