from rest_framework import serializers
from .models import Book, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    genres = GenreSerializer(many=True, read_only=True)
    downloads_count = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'cover', 'file',
            'author', 'genres', 'downloads_count', 'created_at'
        ]


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'description', 'cover', 'file', 'genres']