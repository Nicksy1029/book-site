from django.db import models #импорт главного модуля для создания моделей
from django.contrib.auth.models import AbstractUser #импорт заготовки от Джанго

class CustomUser(AbstractUser):
    #создание фиксированного списка вориантов
    class Role(models.TextChoices): #уникальные поля, которых нет в дефолтном User от джанго
        READER = 'READER', 'Читатель' #Используем AbstractUser чтобы добавить свои поля
        AUTHOR = 'AUTHOR', 'Автор' #к дефолтному класу User от джанго
        ADMIN = 'ADMIN', 'Администратор' #первый аргумент сохраняется в таблице БД, а второй - плашка в админке

    role = models.CharField( #создает текстовую колонну в таблице БД
        max_length=15, #Ограничивает длину хранимого текста
        choices=Role.choices, #ограничивает выбор значений значениями класса Role
        default=Role.READER, #дефолтная роль
        verbose_name='Роль', #название поля для отображения в админ-панели на русском языке
    )

    class Meta: #вложенный класс для админки
        verbose_name = "User" #название модели в единственном числе
        verbose_name_plural = "Users" #название модели в множественном числе

