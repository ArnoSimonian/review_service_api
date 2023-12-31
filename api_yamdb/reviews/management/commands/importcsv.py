import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Review, Title, User)

TABLES = {
    User: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    GenreTitle: 'genre_title.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        try:
            for model, csv_f in TABLES.items():
                with open(
                    f'{settings.BASE_DIR}/static/data/{csv_f}',
                    'r',
                    encoding='utf-8'
                ) as csv_file:
                    reader = csv.DictReader(csv_file)
                    model.objects.bulk_create(
                        model(**data) for data in reader)
            self.stdout.write(self.style.SUCCESS('Все данные загружены'))
        except FileNotFoundError as er:
            print(f"Возникла ошибка. Проверьте директорию. Файл не найден\n"
                  f"{er}")
        except Exception as error:
            print("Ошибка")
            print(error)
