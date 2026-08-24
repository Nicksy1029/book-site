from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from .models import Book, Genre
from .serializers import GenreSerializer, BookSerializer, BookCreateSerializer

from django.shortcuts import render

class IsAuthorRole(permissions.BasePermission):
    """
    Кастомное разрешение: читать могут все,
    а загружать книги — только авторизованные пользователи с ролью AUTHOR.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'AUTHOR'


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Эндпоинт для просмотра списка жанров.
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet для просмотра, поиска, создания и скачивания книг.
    """
    permission_classes = [IsAuthorRole]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_queryset(self):
        # В общем списке выводим ТОЛЬКО одобренные модератором книги
        return Book.objects.filter(is_approved=True)

    def get_serializer_class(self):
        # Для создания книги берем BookCreateSerializer, для просмотра — BookSerializer
        if self.action == 'create':
            return BookCreateSerializer
        return BookSerializer

    def perform_create(self, serializer):
        # При сохранении автоматически назначаем автором текущего юзера
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def download(self, request, pk=None):
        book = self.get_object()
        # .add() автоматически игнорирует дубликаты
        book.downloaded_by.add(request.user)
        return Response({
            'file_url': book.file.url,
            'downloads_count': book.downloads_count
        })

# Страница каталога доступна только авторизованным

def catalog_page_view(request):
    return render(request, 'library.html')