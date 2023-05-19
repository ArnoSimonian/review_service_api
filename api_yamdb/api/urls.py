from django.urls import path, include
from rest_framework import routers

from .views import (
    UserViewSet,
    CommentViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    MyTokenObtainApiView,
    TitleViewSet,
    UserRegistrationView)

app_name = 'api'

v1_router = routers.DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/',
         MyTokenObtainApiView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/signup/', UserRegistrationView.as_view(), name='signup')
]
