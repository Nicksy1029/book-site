from rest_framework import serializers #базовый модуль сериалайзера DRF
from .models import CustomUser # импорт модели

#отвечает за прием данных от незалогиненного пользователя при регистрации, их проверку и сохранение нового юзера в БД
class RegisterSerializer(serializers.ModelSerializer): # с помощью ModelSerializer DRF посмотрит на модель и самостоятельно поймет какие типы данных должны быть у полей
    class Meta: #с чем именно работаем
        model = CustomUser
        fields = ('username', 'password', 'email', 'role') # список разрешенных полей, которые принимаем от фронтеда
        extra_kwargs = {
            'password': {'write_only': True} # только для записи, пароль можно только отправить НА сервер при регистрации, но сервер обратно его никогда не отправляет
        }

    def create(self, validated_data): # создаем юзера с провереннми данными
        user = CustomUser.objects.create_user(**validated_data) #create_user хеширует пароль
        return user # **validated_data превращает словарь validated_data в именованые аргументы

# отдача данных на фронтенд когда пользователь заходит в свой профиль
class ProfileUser(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role') # список выгружаемых полей из бд