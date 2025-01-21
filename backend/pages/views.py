from django.shortcuts import render
from django.views.generic import TemplateView
import base64


def my_view(request):
    html_content = "<h1>Секретная информация</h1>"
    # encoded_html = base64.b64encode(html_content.encode()).decode()
    encoded_html = base64.b64encode(html_content.encode()).decode()
    print(encoded_html)
    return render(request, 'pages/test.html', {'encoded_html': encoded_html})


class About(TemplateView):
    template_name = 'pages/about.html'


def page_not_found(request, exception):
    """Ошибка 404"""
    return render(request, 'pages/404.html', status=404)


def error_500(request):
    """Ошибка 500"""
    return render(request, 'pages/500.html', status=500)


def csrf_failure(request, reason=''):
    """Ошибка 403"""
    return render(request, 'pages/403csrf.html', status=403)
