from django.core.management.base import BaseCommand, CommandError
from coursereg.models import Degree
import json

class Command(BaseCommand):
    help = 'Bulk load degrees to the database from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('--datafile',
            default='coursereg/data/degrees.json',
            help='File to load data from (default: coursereg/data/degrees.json)')

    def handle(self, *args, **options):
        with open(options['datafile']) as f:
            degrees = json.loads(f.read())
            counter = 0
            for degree in degrees:
                degree_name = degree['name']
                is_active = degree['is_active']
                if not Degree.objects.filter(name=degree_name):
                    Degree.objects.create(name=degree_name, is_active=is_active)
                    counter += 1
            self.stdout.write(self.style.SUCCESS(
                'Successfully added %s degrees to the databse.' % (counter, )
            ))            
