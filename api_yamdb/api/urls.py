from django.urls import path, include
from rest_framework.routers import SimpleRouter

from api.views import CommentViewSet, CategoryViewSet, GenreViewSet, ReviewViewSet, TitleViewSet

app_name = 'api'

router = SimpleRouter()
router.register('v1/genres', GenreViewSet, basename='genres')
router.register('v1/categories', CategoryViewSet, basename='categories')
router.register('v1/titles', TitleViewSet, basename='titles')
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('', include(router.urls)),
]
