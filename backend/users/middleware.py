import threading


local = threading.local()


def is_from_admin():
    """Проверяет, был ли запрос из админки."""
    return getattr(local, "from_admin", False)


class AdminActionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Устанавливаем флаг, если запрос из админки
        local.from_admin = request.path.startswith("/admin/")
        response = self.get_response(request)
        local.from_admin = False  # Сбрасываем флаг после обработки запроса
        return response
