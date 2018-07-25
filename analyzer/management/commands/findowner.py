from django.core.management.base import BaseCommand
from analyzer.management.calculations.ownerfinder import OwnerFinder
import warnings


class Command(BaseCommand):

    def handle(self, *args , **options):

        warnings.warn("To try different sentences change the sample text from ml/management/commands/findowner/.")

        sample_text = "Vronsky’s life was particularly happy in that he had a code of principles, which defined with unfailing certitude what he ought and what he ought not to do."
        owner = OwnerFinder.find_owner(sample_text)

        print(owner)
