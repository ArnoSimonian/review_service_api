from rest_framework import viewsets

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title, User
from .serializers import UserSerializer, CategorySerializer, GenreSerializer, TitleSerializer


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
