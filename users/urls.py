from django.urls import path

from .views import ProfileUserView, RegisterView, login_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('me/', ProfileUserView.as_view(), name='me'),
]