import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (Category, Comment, Genre,
                            Review, Title, User)
from reviews.validators import validate_name


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]

    def validate_username(self, value):
        return validate_name(value)


class MeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=('name', 'slug'),
                message="Поле slug каждой категории должно быть уникальным."
            )
        ]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=('name', 'slug'),
                message="Поле slug каждого жанра должно быть уникальным."
            )
        ]


class TitleRetrieveListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='slug',
                                queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='slug',
                             queryset=Genre.objects.all(),
                             many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError(
                "Год выпуска произведения не может быть больше текущего.")
        return value

    # def validate(self, data):
    #     data = Title.objects.filter(
    #         id=self.context['view'].kwargs.get('title_id'))
    #     if 'genre' not in data:
    #         raise serializers.ValidationError(
    #             "Жанр - обязательное поле.")

        # if self.context['request'].method == 'POST' and (
        #     Review.objects.select_related('author', 'title').filter(
        #     title_id=self.context['view'].kwargs.get('title_id'),
        #     author=self.context['request'].user).exists()):
        #     raise serializers.ValidationError(
        #         "Нельзя оставить отзыв к одному произведению дважды."
        #     )
        # return data

    def to_representation(self, instance):
        return TitleRetrieveListSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'POST' and (
                Review.objects.select_related('author', 'title').filter(
                    title_id=self.context['view'].kwargs.get('title_id'),
                    author=self.context['request'].user).exists()):
            raise serializers.ValidationError(
                "Нельзя оставить отзыв к одному произведению дважды."
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)

    def validate_username(self, value):
        return validate_name(value)


class MyTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    def validate_username(self, value):
        return validate_name(value)
