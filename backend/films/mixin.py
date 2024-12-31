from django.shortcuts import redirect
from .models import FilmsdModel
from django.contrib import messages
from django.urls import reverse_lazy


class OnlyAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        coment = self.get_object()
        if coment.author != self.request.user:
            return redirect(
                'films:film', kwargs['film_id_kp']
            )
        return super().dispatch(request, *args, **kwargs)


class FilmMixin:
    def dispatch(self, request, *args, **kwargs):
        result = FilmsdModel.objects.filter(
            id_kp=self.kwargs[self.pk_url_kwarg]).first()
        if not result:
            messages.error(request, (
                'Фильма нет в базе. Нажмите «Отправить на проверку» '
                'и после проверки его добавим.'))
            # return redirect(reverse_lazy(
            #     'films:add_film',
            #     kwargs={'id': self.kwargs[self.pk_url_kwarg]})
            # )
            return redirect(
                reverse_lazy('films:add_film')
                + f'?id={self.kwargs[self.pk_url_kwarg]}')

        if not result.verified and not result.is_published:
            messages.info(request, (
                'Фильм уже существует в базе, но еще не опубликован. '
                'После проверки его сделаем доступным.'))
            return redirect(reverse_lazy('films:add_film'))
        return super().dispatch(request, *args, **kwargs)
