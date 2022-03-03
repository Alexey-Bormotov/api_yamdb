import csv

from django.core.management.base import BaseCommand

from reviews.models import Genres, Titles, GenresTitles

class Command(BaseCommand):
    help = 'Импорт данных из csv в модель GenresTitles'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Путь к файлу')

    def handle(self, *args, **options):
        file_path = options['path']
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                genre = Genres.objects.get(pk=row[2])
                title = Titles.objects.get(pk=row[1])
                GenresTitles.objects.create(
                    id=row[0],
                    genre=genre,
                    title=title,
                )
