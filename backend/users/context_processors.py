from .models import Message


def unread_messages_count(request):
    """Возвращает количество непрочитанных сообщений текущего пользователя."""
    if request.user.is_authenticated:
        count = Message.objects.filter(
            receiver=request.user, is_read=False).count()
        return {'unread_messages_count': count}
    return {'unread_messages_count': 0}
