from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests

# Базовый URL для вашего FastAPI сервера
FASTAPI_BASE_URL = "http://web:8000"


class SyncUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Создаём пользователя без проверки существования
        user = CustomUser.objects.create(username=username)
        user.set_password(password)
        user.save()

        return Response({'message': f'Пользователь {username} успешно синхронизирован.'},
                        status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Неверное имя пользователя или пароль.'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)


class UploadImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        image = request.data.get('file')

        fastapi_url = f"{settings.FASTAPI_BASE_URL}/upload_doc/"
        files = {'file': (image.name, image, image.content_type)}

        response = requests.post(fastapi_url, files=files)

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)
        return Response({'error': response.json().get('detail', 'Ошибка загрузки.')}, status=response.status_code)


class DeleteDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, doc_id):
        fastapi_delete_url = f"{FASTAPI_BASE_URL}/doc_delete/{doc_id}/"
        fastapi_response = requests.delete(fastapi_delete_url)

        if fastapi_response.status_code == 200:
            return Response({"message": "Документ успешно удалён."}, status=status.HTTP_200_OK)

        return Response(
            {"error": fastapi_response.json().get('detail', 'Ошибка удаления.')},
            status=fastapi_response.status_code
        )

class AnalyzeDocumentView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, doc_id):
        fastapi_analyze_url = f"{FASTAPI_BASE_URL}/doc_analyse/{doc_id}/"
        fastapi_response = requests.put(fastapi_analyze_url)

        if fastapi_response.status_code == 200:
            response_data = fastapi_response.json()
            return Response(
                {"message": "Анализ документа успешно запущен.", "details": response_data},
                status=status.HTTP_200_OK
            )
        return Response(
            {"error": fastapi_response.json().get('detail', 'Ошибка анализа.')},
            status=fastapi_response.status_code)

class GetDocumentTextView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doc_id):
        # fastapi_get_text_url = f"{FASTAPI_BASE_URL}/get_text/{doc_id}"

        # Добавляем токен в заголовок для аутентификации
        # headers = {
        #     'Authorization': f'Bearer {request.auth}'  # Используем токен из запроса
        # }

        response = requests.get(f"{FASTAPI_BASE_URL}/get_text/{doc_id}")

        if response.status_code == 200:
            return Response(response.json(), status=status.HTTP_200_OK)

        return Response(
            {'error': response.json().get('detail', 'Ошибка получения текста.')},
            status=response.status_code)