import csv

from django.core.management.base import BaseCommand

from users.models import User
from reviews.models import Comment, Review


class Command(BaseCommand):
    help = 'Импорт данных из csv в модель Comment'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Путь к файлу')

    def handle(self, *args, **options):
        file_path = options['path']
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                review = Review.objects.get(pk=row[1])
                author = User.objects.get(pk=row[3])
                Comment.objects.create(
                    id=row[0],
                    review=review,
                    text=row[2],
                    author=author,
                    pub_date=row[4],
                )
