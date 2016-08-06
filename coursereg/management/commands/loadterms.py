from django.core.management.base import BaseCommand, CommandError
from coursereg.models import Term
import json

class Command(BaseCommand):
    help = 'Bulk load term to the database from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('--datafile',
            default='coursereg/data/terms.json',
            help='File to load data from (default: coursereg/data/terms.json)')

    def handle(self, *args, **options):
        with open(options['datafile']) as f:
            terms = json.loads(f.read())
            counter = 0
            for term in terms:
                name = term['name']
                is_active = term['is_active']
                if not Term.objects.filter(name=name):
                    Term.objects.create(name=name, is_active=is_active)
                    counter += 1
            self.stdout.write(self.style.SUCCESS(
                'Successfully added %s terms to the databse.' % (counter, )
            ))                                                                                
