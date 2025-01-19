from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import Http404
from .models import FilmsdModel, Coment


class OnlyAuthorMixin:
    def dispatch(self, request, *args, **kwargs):
        coment = self.get_object()
        if coment.author != self.request.user:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class CommentMixin:
    model = Coment
    template_name = 'films/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_queryset(self):
        return super().get_queryset().filter(
            pk=self.kwargs['comment_id'],
        )

    def get_success_url(self):
        return reverse(
            'films:film', kwargs={'id_kp': self.kwargs['film_id_kp']}
        )


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
