class LogUnauthorizedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            # Логируем заголовки для неавторизованных запросов
            print(f"Unauthorized request headers: {request.headers}")
        return self.get_response(request)