from django.core.management.base import BaseCommand, CommandError
from coursereg.models import RegistrationType
import json
from django.utils import timezone
from datetime import timedelta, datetime


class Command(BaseCommand):
    help = 'Bulk load term to the database from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('--datafile',
            default='coursereg/data/registration_types.json',
            help='File to load data from (default: coursereg/data/registration_types.json)')

    def handle(self, *args, **options):
        with open(options['datafile']) as f:
            reg_types = json.loads(f.read())
            counter = 0
            for reg_type in reg_types:
                name = reg_type['name']
                if not RegistrationType.objects.filter(name=name):
                    RegistrationType.objects.create(
                        name=name,
                        should_count_towards_cgpa=reg_type['should_count_towards_cgpa'],
                        is_active=reg_type['is_active']
                    )
                    counter += 1
            self.stdout.write(self.style.SUCCESS(
                'Successfully added %s registration types to the databse.' % (counter, )
            ))                                                                                
