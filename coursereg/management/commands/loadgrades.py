from django.core.management.base import BaseCommand, CommandError
from coursereg.models import Grade
import json

class Command(BaseCommand):
    help = 'Bulk load grades to the database from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('--datafile',
            default='coursereg/data/grades.json',
            help='File to load data from (default: coursereg/data/grades.json)')

    def handle(self, *args, **options):
        with open(options['datafile']) as f:
            grades = json.loads(f.read())
            counter = 0
            for grade in grades:
                name = grade['name']
                points = grade['points']
                should_count_towards_cgpa = grade['should_count_towards_cgpa']
                if not Grade.objects.filter(name=name):
                    Grade.objects.create(name=name, points=points, should_count_towards_cgpa=should_count_towards_cgpa)
                    counter += 1
            self.stdout.write(self.style.SUCCESS(
                'Successfully added %s grades to the databse.' % (counter, )
            ))                                                                                
