from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название жанра")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название книги")
    description = models.TextField(blank=True, verbose_name="Описание")

    # Файлы и картинки
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name="Обложка")
    downloaded_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downloaded_books', blank=True)  # Уникальные скачивания
    file = models.FileField(
        upload_to='books_pdf/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name="Файл PDF"
    )

    # Связи
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_books',
        verbose_name="Автор/Загрузчик"
    )
    genres = models.ManyToManyField(Genre, related_name='books', verbose_name="Жанры")

    # Модерация и статистика
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено модерацией")
    downloads_count = models.PositiveIntegerField(default=0, verbose_name="Количество скачиваний")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    @property
    def downloads_count(self):
        return self.downloaded_by.count()

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
