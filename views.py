from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from .models import CustomUser
from django.urls import reverse
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
import os

User = get_user_model()

logger = logging.getLogger(__name__)

# Базовый URL для вашего FastAPI сервера
FASTAPI_BASE_URL = "http://web:8000"



class RegisterView(APIView):
    """
    Эндпоинт для регистрации нового пользователя.
    """

    def post(self, request):
        logger.debug("Запрос на регистрацию: %s", request.data)

        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            logger.warning("Не указаны имя пользователя или пароль в запросе.")
            return Response(
                {'error': 'Необходимо указать имя пользователя и пароль.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if CustomUser.objects.filter(username=username).exists():
            logger.warning(f"Попытка регистрации существующего пользователя: {username}")
            return Response(
                {'error': 'Пользователь с таким именем уже существует.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создаём нового пользователя
        user = CustomUser.objects.create(username=username)
        user.set_password(password)
        user.save()

        logger.info(f"Новый пользователь создан: {username}")
        return Response(
            {'message': f'Пользователь {username} успешно зарегистрирован.'},
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    """
    Эндпоинт для аутентификации пользователя и выдачи токенов.
    """

    def post(self, request):
        logger.debug("Запрос на аутентификацию: %s", request.data)

        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            logger.warning("Не указаны имя пользователя или пароль в запросе.")
            return Response(
                {'error': 'Необходимо указать имя пользователя и пароль.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, существует ли пользователь и правильный ли пароль
        user = authenticate(username=username, password=password)
        if not user:
            logger.warning(f"Неверный логин или пароль для пользователя {username}")
            return Response(
                {'error': 'Неверное имя пользователя или пароль.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Генерируем токены для пользователя
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        # Сохранение токенов в модель пользователя
        user.auth_token = str(access)
        user.refresh_token = str(refresh)
        user.save()

        logger.info(f"Пользователь {username} успешно аутентифицирован. Токены выданы.")
        return Response(
            {
                'refresh': str(refresh),
                'access': str(access),
                'message': 'Аутентификация успешна.'
            },
            status=status.HTTP_200_OK
        )

class UploadImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.debug("Получен запрос на загрузку файла.")

        if 'file' not in request.data:
            return Response(
                {'error': 'Файл не предоставлен.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        image = request.data['file']
        logger.info(f"Файл '{image.name}' получен для загрузки.")

        # Получаем токен доступа из заголовка Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response(
                {'error': 'Токен доступа не предоставлен.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = auth_header.split('Bearer ')[1]

        # Проверяем токен через эндпоинт TokenVerifyView
        verify_url = request.build_absolute_uri(reverse('token_verify'))
        response = requests.post(verify_url, data={'token': access_token})

        if response.status_code != 200:
            logger.info("Токен доступа истёк. Попытка обновить токен...")
            new_tokens = refresh_access_token(request)
            if not new_tokens:
                return Response(
                    {'error': 'Не удалось обновить токен доступа.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            access_token = new_tokens['access']
            # Обновляем токен в заголовке для отправки запроса на FastAPI
            auth_header = f'Bearer {access_token}'

        # URL для загрузки документа на FastAPI
        fastapi_upload_url = f"{FASTAPI_BASE_URL}/upload_doc/"

        # Отправляем файл на FastAPI
        try:
            files = {
                'file': (image.name, image, image.content_type or 'application/octet-stream')
            }
            headers = {
                'Authorization': auth_header  # Используем обновлённый токен
            }
            response = requests.post(fastapi_upload_url, files=files, headers=headers)

            if response.status_code == 200:
                logger.info(f"Файл '{image.name}' успешно загружен на FastAPI сервер.")

                # Получаем fastapi_doc_id из ответа FastAPI
                response_data = response.json()
                fastapi_doc_id = response_data.get('id')

                if not fastapi_doc_id:
                    logger.error("Ответ FastAPI не содержит fastapi_doc_id.")
                    return Response(
                        {'error': 'Ответ FastAPI не содержит идентификатор документа.'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                # Сохраняем fastapi_doc_id в CustomUser
                request.user.fastapi_doc_id = fastapi_doc_id
                request.user.save()
                logger.info(f"fastapi_doc_id={fastapi_doc_id} успешно сохранён для пользователя {request.user.username}.")

                # Возвращаем ответ клиенту
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                logger.error(
                    f"Ошибка при загрузке файла '{image.name}' на FastAPI сервер: "
                    f"{response.status_code} {response.text}"
                )
                return Response(
                    {'error': f'Ошибка FastAPI: {response.text}'},
                    status=response.status_code
                )
        except requests.RequestException as e:
            logger.error(f"Ошибка при отправке запроса на FastAPI: {e}")
            return Response(
                {'error': 'Ошибка при связи с backend сервером.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def refresh_access_token(request):
    """
    Обновляет токен доступа, используя refresh-токен из заголовка.
    """
    try:
        # Получаем refresh-токен из заголовка Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # Refresh-токен отсутствует в заголовке

        # Извлекаем токен
        refresh_token = auth_header.split('Bearer ')[1]

        # Создаем объект RefreshToken
        refresh = RefreshToken(refresh_token)

        # Генерируем новый access-токен
        new_access_token = str(refresh.access_token)

        # Возвращаем новый токен
        return {'access': new_access_token,}

    except TokenError as e:
        logger.error(f"Ошибка обновления токена доступа: {e}")
        return None
    except Exception as e:
        logger.error(f"Общая ошибка при обновлении токена: {e}")
        return None

class GetDocumentTextView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, doc_id):
        logger.debug(f"Получен запрос на получение текста документа с ID {doc_id}.")

        # Получаем токен доступа из заголовка Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response(
                {'error': 'Токен доступа не предоставлен.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        access_token = auth_header.split('Bearer ')[1]

        # Проверяем токен через эндпоинт TokenVerifyView
        verify_url = request.build_absolute_uri(reverse('token_verify'))
        response = requests.post(verify_url, data={'token': access_token})

        if response.status_code != 200:
            logger.info("Токен доступа истёк. Попытка обновить токен...")
            new_tokens = refresh_access_token(request)
            if not new_tokens:
                return Response(
                    {'error': 'Не удалось обновить токен доступа.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            access_token = new_tokens['access']
            # Обновляем токен в заголовке для отправки запроса на FastAPI
            auth_header = f'Bearer {access_token}'

        # URL для получения текста документа с FastAPI
        fastapi_get_text_url = f"{FASTAPI_BASE_URL}/get_text/{doc_id}/"

        # Отправляем запрос на FastAPI для получения текста документа
        try:
            headers = {
                'Authorization': auth_header  # Используем обновлённый токен
            }
            response = requests.get(fastapi_get_text_url, headers=headers)

            if response.status_code == 200:
                logger.info(f"Текст документа с ID {doc_id} успешно получен с FastAPI сервера.")
                return Response(response.json(), status=status.HTTP_200_OK)
            else:
                logger.error(
                    f"Ошибка при получении текста документа с ID {doc_id} с FastAPI сервера: "
                    f"{response.status_code} {response.text}"
                )
                return Response(
                    {'error': f'Ошибка FastAPI: {response.text}'},
                    status=response.status_code
                )
        except requests.RequestException as e:
            logger.error(f"Ошибка при отправке запроса на FastAPI: {e}")
            return Response(
                {'error': 'Ошибка при связи с backend сервером.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteDocumentView(APIView):
    """
    Ручка для удаления документа через FastAPI.
    Удаляет файл
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, doc_id):
        # Лог: начало обработки запроса
        logger.info(f"Поступил запрос на удаление документа с ID {doc_id} от пользователя {request.user}.")

        # URL для удаления документа в FastAPI
        fastapi_delete_url = f"{FASTAPI_BASE_URL}/doc_delete/{doc_id}/"

        # Проверяем наличие токена авторизации
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.error("Токен авторизации не предоставлен.")
            return Response(
                {"error": "Токен авторизации не предоставлен."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Отправляем запрос DELETE к FastAPI
            headers = {'Authorization': auth_header}
            logger.debug(f"Отправка запроса DELETE на {fastapi_delete_url} с заголовками: {headers}")
            fastapi_response = requests.delete(fastapi_delete_url, headers=headers)

            if fastapi_response.status_code == 200:
                # Лог: успешное удаление документа в FastAPI
                logger.info(f"Документ с ID {doc_id} успешно удалён на FastAPI.")

                # Если файл был удалён на стороне FastAPI, удаляем локальный файл
                response_data = fastapi_response.json()
                file_path = response_data.get("file_path")  # Если нужно получать путь к файлу
                if file_path:
                    absolute_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
                    if os.path.exists(absolute_file_path):
                        os.remove(absolute_file_path)
                        # Лог: успешное удаление локального файла
                        logger.debug(f"Файл {absolute_file_path} успешно удалён с локального диска.")
                    else:
                        # Лог: файл не найден на локальном диске
                        logger.warning(f"Файл {absolute_file_path} не найден на локальном диске.")

                return Response(
                    {"message": "Документ успешно удалён."},
                    status=status.HTTP_200_OK
                )
            else:
                # Лог: ошибка удаления на стороне FastAPI
                logger.error(
                    f"Ошибка при удалении документа в FastAPI. "
                    f"Код ответа: {fastapi_response.status_code}. Ответ: {fastapi_response.text}"
                )
                return Response(
                    {"error": f"Ошибка FastAPI: {fastapi_response.json().get('detail', 'Неизвестная ошибка')}"},
                    status=fastapi_response.status_code
                )

        except requests.RequestException as e:
            # Лог: ошибка соединения с FastAPI
            logger.error(f"Ошибка связи с FastAPI при удалении документа с ID {doc_id}: {e}")
            return Response(
                {"error": "Ошибка связи с FastAPI сервером."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class AnalyzeDocumentView(APIView):
    """
    Ручка для анализа документа через FastAPI.
    Запускает процесс анализа документа на FastAPI.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, doc_id):
        # Лог: начало обработки запроса
        logger.info(f"Поступил запрос на анализ документа с ID {doc_id} от пользователя {request.user}.")

        # URL для анализа документа в FastAPI
        fastapi_analyze_url = f"{FASTAPI_BASE_URL}/doc_analyse/{doc_id}/"


        # Проверяем наличие токена авторизации
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            logger.error("Токен авторизации не предоставлен.")
            return Response(
                {"error": "Токен авторизации не предоставлен."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # Отправляем запрос PUT к FastAPI
            headers = {'Authorization': auth_header}
            logger.debug(f"Отправка запроса PUT на {fastapi_analyze_url} с заголовками: {headers}")
            fastapi_response = requests.put(fastapi_analyze_url, headers=headers)

            if fastapi_response.status_code == 200:
                # Лог: успешный запуск анализа документа на FastAPI
                logger.info(f"Анализ документа с ID {doc_id} успешно запущен на FastAPI.")
                response_data = fastapi_response.json()

                return Response(
                    {"message": "Анализ документа успешно запущен.", "details": response_data},
                    status=status.HTTP_200_OK
                )
            else:
                # Лог: ошибка анализа на стороне FastAPI
                logger.error(
                    f"Ошибка при анализе документа в FastAPI. "
                    f"Код ответа: {fastapi_response.status_code}. Ответ: {fastapi_response.text}"
                )
                return Response(
                    {"error": f"Ошибка FastAPI: {fastapi_response.json().get('detail', 'Неизвестная ошибка')}"},
                    status=fastapi_response.status_code
                )

        except requests.RequestException as e:
            # Лог: ошибка соединения с FastAPI
            logger.error(f"Ошибка связи с FastAPI при анализе документа с ID {doc_id}: {e}")
            return Response(
                {"error": "Ошибка связи с FastAPI сервером."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )