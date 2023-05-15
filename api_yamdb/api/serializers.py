import re

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreTitle,
                            Review,
                            Title,
                            User,
                            CHOICES)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = User
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TitleRetrieveListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']
        if not rating:
            return None
        return round(rating)


class TitleCreateSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(slug_field='name',
                                queryset=Category.objects.all())
    genre = SlugRelatedField(slug_field='name',
                             queryset=Genre.objects.all(),
                             many=True)

    class Meta:
        model = Title
        fields = '__all__'


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
        title_id = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(title_id=title_id, author=author).exists():
            raise serializers.ValidationError(
                'Нельзя оставить отзыв к одному произведению дважды.'
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


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    # def validate_username(self, value):
    #     reg_expression = re.compile('^[\w.@+-]+\z')
    #     if not reg_expression.match(value):
    #         raise serializers.ValidationError(
    #             'Имя пользователя не соответствует регулярному выражению!'
    #         )
    #     return value


class MyTokenObtainSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        if not User.objects.filter(
                username=data['username'],
                confirmation_code=data['confirmation_code']
        ).exists():
            raise serializers.ValidationError('Пользователь не найден!')
        return data

    # def validate_username(self, value):
    #     reg_expression = re.compile('^[\w.@+-]+\z')
    #     if not reg_expression.match(value):
    #         raise serializers.ValidationError(
    #             'Имя пользователя не соответствует регулярному выражению!'
    #         )
    #     return value
