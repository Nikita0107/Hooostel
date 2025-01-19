from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Добро пожаловать на главную страницу!")

urlpatterns = [
    path('admin', admin.site.urls),  # Админка
    path('', home),  # Корневая страница
    path('api/', include('proxy_app.urls')),  # Подключение маршрутов из приложения proxy_app
]