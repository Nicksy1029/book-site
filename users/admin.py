from django.contrib import admin # сам модуль админки Django
from django.contrib.auth.admin import UserAdmin # класс управления пользователями
from .models import CustomUser

@admin.register(CustomUser) # регистрируем модель
class CustomUserAdmin(UserAdmin): # класс настроек админки, наследуем от UserAdmin для работы с юзерами
    list_display = ('username', 'role', 'is_staff', 'is_active') # колонки в общей таблице пользователей
    search_fields = ('username', ) # поисковая строка над таблицей для поиска по логину
    list_filter = ('is_active', 'role', 'is_staff') # панель фильтрации

    fieldsets = UserAdmin.fieldsets + ( # Отвечает поля на странице редактирования конкретного пользователя
        ('Дополнительно', {'fields': ('role',)}), # Берем стандартные поля и делаем дополнительные
    )