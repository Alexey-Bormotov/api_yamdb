import csv

from django.core.management.base import BaseCommand

from reviews.models import Categories, Titles

class Command(BaseCommand):
    help = 'Импорт данных из csv в модель Titles'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Путь к файлу')

    def handle(self, *args, **options):
        file_path = options['path']
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                category = Categories.objects.get(pk=row[3])
                Titles.objects.create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=category,
                )
