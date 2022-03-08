import csv

from django.core.management.base import BaseCommand

from reviews.models import Genre, Title, GenreTitle


class Command(BaseCommand):
    help = 'Импорт данных из csv в модель GenreTitle'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Путь к файлу')

    def handle(self, *args, **options):
        file_path = options['path']
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                genre = Genre.objects.get(pk=row[2])
                title = Title.objects.get(pk=row[1])
                GenreTitle.objects.create(
                    id=row[0],
                    genre=genre,
                    title=title,
                )
