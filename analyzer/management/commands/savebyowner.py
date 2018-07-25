from django.core.management.base import BaseCommand
from analyzer.management.calculations.classifybyowner import ClassifyByOwner

class Command(BaseCommand):
    help = 'partitions the data in database into specified number of bins'

    def handle(self, *args, **options):
        classifier = ClassifyByOwner(1000)

        classifier.create_dataset()
        classifier.classify_and_save()
