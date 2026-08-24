from rest_framework.response import Response # Специальный класс DRF, который оборачивает данные в правильный HTTP-ответ в формате JSON
from rest_framework import generics # Набор готовых "универсальных" вьюшек DRF
from .models import CustomUser
from .serializers import RegisterSerializer, ProfileUser
from rest_framework.permissions import AllowAny, IsAuthenticated #классы прав доступа
from rest_framework.views import APIView #Базовый класс DRF для создания кастомных эндпоинтов, где мы вручную прописываем логику методов
from rest_framework.authtoken.views import ObtainAuthToken # Встроенный механизм DRF для работы с токенами авторизации.
from rest_framework.authtoken.models import Token

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all() #с какой моделью работает вьюшка
    serializer_class = RegisterSerializer # какой сериалайзер проверяет входные данные и хэширует пароль
    permission_classes = [AllowAny] # регистрироваться может любой
    authentication_classes = [] # отключаем проверки авторизации

class CustomObtainAuthToken(ObtainAuthToken): # Наследуем от встроенного класса дрф, который умеет проверять логин и пароль
    authentication_classes = []  # Отключаем сессии и проверку CSRF

    def post(self, request, *args, **kwargs): # переделываем метод обработки пост запроса
        serializer = self.serializer_class(data=request.data, context={'request': request}) #создаем объект сериалайзера
        #serializer.is_validate_serializer = True
        serializer.is_valid(raise_exception=True) #проверка пароля и логина
        user = serializer.validated_data['user'] #достает объект пользователя после аутентификации
        token, created = Token.objects.get_or_create(user=user) # ищет токен пользоателя в базе или создает новый

        return Response({ # отправляем на фронтенд данные и токен
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'role': getattr(user, 'role', 'USER')
        })
login_view = CustomObtainAuthToken.as_view() #упаковка класса в формат функции, который понятен Django (для urls)

class ProfileUserView(APIView):
    permission_classes = [IsAuthenticated] #если пользователь зареган и имеет токен
    def get(self, request): # обработка get-запроса
        serializer = ProfileUser(request.user) # передаем объект юзера в сериалайзер, превращаем в словарь Python
        return Response(serializer.data) # Отдаем JSON с данными профиля на фронтенд
