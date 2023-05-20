import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import action

from reviews.models import (Category,
                            Comment,
                            Genre,
                            GenreTitle,
                            Review,
                            Title,
                            User)
from .filters import TitleFilter
from .permissions import IsAdminOrReadOnly, \
    IsAuthorOrAdminOrModeratorOrReadOnly, IsAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MyTokenObtainSerializer,
                          ReviewSerializer, TitleCreateSerializer,
                          TitleRetrieveListSerializer, UserSerializer,
                          UserRegistrationSerializer, MeSerializer)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(methods=['GET', 'PATCH'],
            detail=False,
            permission_classes=(IsAuthenticated,),
            url_path='me')
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        if request.method == 'PATCH':
            serializer = MeSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleCreateSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleRetrieveListSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrAdminOrModeratorOrReadOnly,)

    # pagination_class = PageNumberPagination

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrModeratorOrReadOnly,)

    # pagination_class = PageNumberPagination

    def get_review(self):
        return get_object_or_404(Review,
                                 id=self.kwargs.get('review_id'),
                                 title_id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()


class UserRegistrationView(APIView):
    def get_confirmation_code(self):
        return str(random.randrange(1000, 9999, 1))

    def send_email(self, email, confirmation_code):
        send_mail(
            'confirmation_code',
            message=confirmation_code,
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        # if User.objects.get(username=serializer.initial_data['username'],
        #                     email=serializer.initial_data['email']).exists():
        #     return Response({'user': 'Такой пользователь уже есть в базе'},
        #                     status=status.HTTP_200_OK)
        if serializer.is_valid():
            confirmation_code = self.get_confirmation_code()
            self.send_email(serializer.validated_data['email'],
                            confirmation_code)
            serializer.save(confirmation_code=confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainApiView(APIView):
    def post(self, request):
        serializer = MyTokenObtainSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            try:
                user = User.objects.get(username=username,
                                        confirmation_code=confirmation_code)
            except User.DoesNotExist:
                return Response({'username': 'Пользователь не найден!'},
                                status=status.HTTP_404_NOT_FOUND)
            access_token = AccessToken.for_user(user)
            return Response({'token': str(access_token)},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
