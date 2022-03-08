import csv

from django.core.management.base import BaseCommand

from users.models import User
from reviews.models import Title, Review


class Command(BaseCommand):
    help = 'Импорт данных из csv в модель Review'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Путь к файлу')

    def handle(self, *args, **options):
        file_path = options['path']
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                title = Title.objects.get(pk=row[1])
                author = User.objects.get(pk=row[3])
                Review.objects.create(
                    id=row[0],
                    title=title,
                    text=row[2],
                    author=author,
                    score=row[4],
                    pub_date=row[5],
                )
