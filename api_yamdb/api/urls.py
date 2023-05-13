from django.urls import path, include
from api.views import GenresViewSet, CategoriesViewSet, TitlesViewSet
from rest_framework.routers import SimpleRouter


app_name = 'api'

router = SimpleRouter()
router.register('v1/genres', GenresViewSet, basename='genres')
router.register('v1/categories', CategoriesViewSet, basename='categories')
router.register('v1/titles', TitlesViewSet, basename='titles')
# router.register(
#    r'v1/posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment')


urlpatterns = [
    path('', include(router.urls)),
]
