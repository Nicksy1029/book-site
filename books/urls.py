from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, GenreViewSet

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'books', BookViewSet, basename='book')

urlpatterns = [
    path('api/', include(router.urls)),
]