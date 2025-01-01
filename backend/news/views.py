from django.conf import settings
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import EventUser
from users.models import Follow
from django.db.models import Subquery, OuterRef


class NewsListView(LoginRequiredMixin, ListView):
    """Список новостей"""
    model = EventUser
    template_name = 'news/index.html'
    pk_url_kwarg = 'username'
    paginate_by = settings.OBJECTS_PER_PAGE * 2

    def get_queryset(self):
        following_users = self.request.user.followers.values_list(
            'following', flat=True)

        following_dates = Follow.objects.filter(
            user=self.request.user,  # подписчик
            following=OuterRef('user')  # тот, на кого подписаны
        ).values('created_at')

        result = self.model.objects.filter(
            user__in=following_users,
            created_at__gte=Subquery(following_dates)
        ).select_related('user')
        return result
