from rest_framework import viewsets

from reviews.models import Categories, Comment, Genres, GenreTitle, Review, Titles, User
from .serializers import UserSerializer, CategoriesSerializer, GenresSerializer, TitlesSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
